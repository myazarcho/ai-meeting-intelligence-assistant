import json
from pathlib import Path

import streamlit as st


BASE_DIR = Path(__file__).resolve().parent
SAMPLE_PATH = BASE_DIR / "sample_data" / "meeting_01.txt"
OUTPUT_PATH = BASE_DIR / "outputs" / "sample_output.json"


def load_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def render_result(result: dict) -> None:
    st.subheader("Meeting Summary")
    st.write(result.get("meeting_summary", "Not available"))

    st.subheader("Key Decisions")
    decisions = result.get("key_decisions", [])
    if decisions:
        for item in decisions:
            st.markdown(f"- {item}")
    else:
        st.write("No confirmed decisions found.")

    st.subheader("Action Items")
    action_items = result.get("action_items", [])
    if action_items:
        st.dataframe(action_items, use_container_width=True)
    else:
        st.write("No action items found.")

    st.subheader("Risks or Blockers")
    risks = result.get("risks_or_blockers", [])
    if risks:
        for item in risks:
            st.markdown(f"- {item}")
    else:
        st.write("No risks or blockers found.")

    st.subheader("Open Questions")
    questions = result.get("open_questions", [])
    if questions:
        for item in questions:
            st.markdown(f"- {item}")
    else:
        st.write("No open questions found.")

    st.subheader("Follow-up Email Draft")
    st.text_area(
        "Generated email",
        value=result.get("follow_up_email", ""),
        height=240,
    )

    st.download_button(
        "Download result as JSON",
        data=json.dumps(result, indent=2, ensure_ascii=False),
        file_name="meeting_analysis.json",
        mime="application/json",
    )


st.set_page_config(
    page_title="AI Meeting Intelligence Assistant",
    page_icon="📝",
    layout="wide",
)

st.title("AI Meeting Intelligence Assistant")
st.caption(
    "Transform an unstructured meeting transcript into a summary, "
    "decisions, action items, deadlines, risks, and a follow-up email."
)

st.info(
    "Version 1 is a portfolio prototype. It displays a prepared sample result "
    "without requiring an API key."
)

sample_text = load_text(SAMPLE_PATH)
sample_result = load_json(OUTPUT_PATH)

transcript = st.text_area(
    "Meeting transcript",
    value=sample_text,
    height=340,
    placeholder="Paste a meeting transcript here...",
)

col1, col2 = st.columns(2)

with col1:
    analyze = st.button("Analyze Meeting", type="primary", use_container_width=True)

with col2:
    clear = st.button("Clear", use_container_width=True)

if clear:
    st.rerun()

if analyze:
    if not transcript.strip():
        st.warning("Please enter a meeting transcript.")
    else:
        st.success("Demo analysis completed.")
        render_result(sample_result)

st.divider()
st.caption(
    "Responsible use: Review all AI-generated information before using it "
    "for official communication or project decisions."
)
