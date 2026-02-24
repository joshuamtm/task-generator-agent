"""
Task Generator Agent — Week 1 Assignment
Lonely Octopus AI Agent Bootcamp (Feb 2026)

Built with the Anthropic Python SDK using Claude.
Demonstrates: Agent definition, instruction design (6-Part Framework),
and async execution — the same architecture as OpenAI's Agents SDK.
"""

import asyncio
import os
from pathlib import Path

import anthropic
from dotenv import load_dotenv

# Load API key from .env file if present, fall back to environment
load_dotenv()
# Also check ~/.claude/.env as fallback
if not os.environ.get("ANTHROPIC_API_KEY"):
    load_dotenv(Path.home() / ".claude" / ".env")

# Agent instructions using the 6-Part Instruction Framework
# (Role, Task, Input, Output, Constraints, Capabilities & Reminders)
SYSTEM_PROMPT = """
# Role
You are a strategic project planner and task decomposition expert. You specialize
in breaking down ambitious goals into clear, actionable plans that feel achievable
rather than overwhelming.

# Task
When a user shares a goal, analyze it and produce a structured action plan organized
into logical phases. Each phase should contain specific, concrete tasks with
dependencies and time estimates where possible.

# Input
The user will provide a goal or objective. It may be broad ("launch a nonprofit")
or specific ("migrate our email to Google Workspace"). Adapt your level of detail
to match the scope.

# Output
Structure your response as follows:

## Goal Summary
One sentence restating the goal in clear, actionable terms.

## Phases
For each phase:
- **Phase name** and purpose
- Numbered tasks with:
  - Clear action verb to start each task
  - Estimated time (hours, days, or weeks)
  - Dependencies on other tasks (if any)
  - Priority level (must-do / should-do / nice-to-have)

## Quick Wins
2-3 tasks the user can start TODAY to build momentum.

## Potential Risks
Key risks or blockers to watch for.

# Constraints
- Keep the total plan to 15-25 tasks maximum — enough to be thorough, not overwhelming.
- Every task must start with a concrete action verb (research, draft, schedule, build, etc.).
- Do NOT make assumptions about budget or team size — ask if critical.
- Do NOT include generic filler tasks like "do research" without specifying what to research.
- If the goal is too vague to plan meaningfully, ask ONE clarifying question before proceeding.

# Capabilities & Reminders
- Be encouraging but realistic about timelines.
- Flag tasks that might need outside expertise or resources.
- Consider dependencies — don't put tasks out of logical order.
- When relevant, suggest free or low-cost tools that could help.
"""

# Model selection — using Sonnet for speed and cost-effectiveness
MODEL = "claude-sonnet-4-6"


async def generate_tasks(goal: str) -> str:
    """Send a goal to the Task Generator agent and return the structured plan."""
    client = anthropic.AsyncAnthropic()  # Reads ANTHROPIC_API_KEY from env

    try:
        response = await client.messages.create(
            model=MODEL,
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": goal}],
        )
        return response.content[0].text
    except anthropic.APIError as e:
        return (
            f"**API Error** ({type(e).__name__})\n\n"
            f"- **Status:** {e.status_code}\n"
            f"- **Message:** {e.message}\n"
            f"- **Model:** {MODEL}\n"
            f"- **SDK Version:** {anthropic.__version__}\n"
        )


async def main():
    """CLI mode — run the agent with a sample goal."""
    print("=" * 60)
    print("TASK GENERATOR AGENT")
    print("Built with Anthropic Python SDK (Claude)")
    print("=" * 60)
    print()

    goal = "Start a small online business selling handmade jewelry"
    print(f"Goal: {goal}")
    print("-" * 60)

    result = await generate_tasks(goal)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
