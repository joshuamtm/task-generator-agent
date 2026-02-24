"""
Task Generator Agent — Streamlit UI
Week 1 Assignment, Lonely Octopus AI Agent Bootcamp

Run: streamlit run app.py
"""

import streamlit as st
import asyncio
from main import generate_tasks
from pdf_export import generate_pdf

st.set_page_config(
    page_title="MTM Task Generator Agent",
    page_icon="📋",
    layout="wide",
)

# --- MTM Branded Header ---
st.markdown(
    """
    <style>
    .mtm-header {
        background: linear-gradient(135deg, #0891b2 0%, #0e7490 50%, #155e75 100%);
        padding: 24px 32px;
        border-radius: 12px;
        margin-bottom: 24px;
        display: flex;
        align-items: center;
        gap: 20px;
    }
    .mtm-header img {
        height: 48px;
    }
    .mtm-header-text h1 {
        color: white;
        font-size: 28px;
        margin: 0;
        font-weight: 700;
    }
    .mtm-header-text p {
        color: rgba(255, 255, 255, 0.85);
        font-size: 14px;
        margin: 4px 0 0 0;
    }
    .mtm-footer {
        text-align: center;
        color: #85abbd;
        font-size: 12px;
        margin-top: 40px;
        padding-top: 16px;
        border-top: 1px solid #e5e7eb;
    }
    .mtm-footer a {
        color: #1ab1d2;
        text-decoration: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.image("mtm-logo.png", width=180)
st.markdown(
    """
    <div style="margin-top: -8px; margin-bottom: 24px;">
        <h1 style="color: #1c487b; font-size: 28px; margin: 0;">Task Generator Agent</h1>
        <p style="color: #85abbd; font-size: 14px; margin: 4px 0 0 0;">
            Built with the Anthropic Python SDK (Claude) &mdash;
            Week 1, Lonely Octopus AI Agent Bootcamp
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

# --- Sidebar ---
with st.sidebar:
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #0891b2, #0e7490, #155e75);
                    padding: 16px; border-radius: 8px; margin-bottom: 16px;">
            <p style="color: white; font-weight: 600; font-size: 16px; margin: 0;">
                Example Goals
            </p>
            <p style="color: rgba(255,255,255,0.8); font-size: 12px; margin: 4px 0 0 0;">
                Click any goal to try it
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    examples = [
        "Start a small online business selling handmade jewelry",
        "Launch a nonprofit mentoring program for first-generation college students",
        "Migrate our 50-person organization from on-premise email to Google Workspace",
        "Plan a fundraising gala for 200 guests with a $15,000 budget",
        "Build a personal website and start freelancing as a graphic designer",
    ]

    for example in examples:
        if st.button(example, key=example):
            st.session_state["goal_input"] = example

    st.markdown("---")
    st.markdown(
        "**How it works:** Enter any goal and the agent breaks it down into "
        "phases, tasks, quick wins, and risk flags."
    )
    st.markdown(
        '<p style="color: #85abbd; font-size: 12px; margin-top: 16px;">'
        "Powered by Claude (Anthropic) via the Python SDK</p>",
        unsafe_allow_html=True,
    )

# --- Main Input ---
goal = st.text_area(
    "What's your goal?",
    value=st.session_state.get("goal_input", ""),
    height=100,
    placeholder="Describe what you want to accomplish...",
)

col1, col2 = st.columns([1, 5])
with col1:
    run_button = st.button("Generate Plan", type="primary")

if run_button and goal.strip():
    with st.spinner("Breaking down your goal into actionable tasks..."):
        result = asyncio.run(generate_tasks(goal.strip()))

    st.markdown("---")
    st.markdown(result)

    st.session_state["last_result"] = result
    st.session_state["last_goal"] = goal.strip()

    pdf_bytes = generate_pdf(result, goal.strip())
    st.download_button(
        label="Download as PDF",
        data=pdf_bytes,
        file_name="task-plan.pdf",
        mime="application/pdf",
    )

elif run_button:
    st.warning("Please enter a goal first.")

if "last_result" in st.session_state and not run_button:
    st.markdown("---")
    st.markdown(f"**Previous goal:** {st.session_state['last_goal']}")
    st.markdown(st.session_state["last_result"])

    pdf_bytes = generate_pdf(
        st.session_state["last_result"], st.session_state["last_goal"]
    )
    st.download_button(
        label="Download as PDF",
        data=pdf_bytes,
        file_name="task-plan.pdf",
        mime="application/pdf",
    )

# --- Footer ---
st.markdown(
    """
    <div class="mtm-footer">
        <a href="https://mtm.now" target="_blank">Meet the Moment</a> &mdash;
        Helping nonprofits harness technology to amplify their impact.
        <br>Built by Joshua Peskay | AI Agent Bootcamp, Feb 2026
    </div>
    """,
    unsafe_allow_html=True,
)
