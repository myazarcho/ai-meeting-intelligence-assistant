import json
from pathlib import Path

import streamlit as st


BASE_DIR = Path(__file__).resolve().parent
SAMPLE_PATH = BASE_DIR / "sample_data" / "meeting_01.txt"
from claude_service import MeetingAnalysisError, analyze_meeting

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

def clear_form() -> None:
    """Clear the transcript and remove the displayed result."""
    st.session_state.transcript = ""
    st.session_state.analysis_result = None
    st.session_state.show_result = False


def load_sample() -> None:
    """Load the included fictional transcript."""
    st.session_state.transcript = load_text(SAMPLE_PATH)
    st.session_state.analysis_result = None
    st.session_state.show_result = False


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

# Initialize application state.
if "transcript" not in st.session_state:
    st.session_state.transcript = ""

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "show_result" not in st.session_state:
    st.session_state.show_result = False

st.title("AI Meeting Intelligence Assistant")

st.caption(
    "Paste your own meeting transcript, or load the included fictional sample."
)

st.info(
    "Version 1 is a UI prototype. It does not use live AI yet. "
    "The Analyze Meeting button displays a prepared sample result "
    "to demonstrate the planned output format."
)


# Transcript controls
left_column, right_column = st.columns(2)

with left_column:
    st.button(
        "Load Sample Transcript",
        on_click=load_sample,
        use_container_width=True,
    )

with right_column:
    st.button(
        "Clear",
        on_click=clear_form,
        use_container_width=True,
    )


# The key connects this widget to st.session_state.transcript.
st.text_area(
    "Meeting transcript",
    key="transcript",
    height=340,
    placeholder="Paste a meeting transcript here...",
)


analyze_button = st.button(
    "Analyze Meeting",
    type="primary",
    use_container_width=True,
)


if analyze_button:
    transcript = st.session_state.transcript.strip()

    if not transcript:
        st.warning(
            "Please paste a transcript or load the sample transcript first."
        )
        st.session_state.show_result = False

    else:
        try:
            with st.spinner("Claude is analyzing the meeting..."):
                result = analyze_meeting(transcript)

            st.session_state.analysis_result = result
            st.session_state.show_result = True
            st.success("Meeting analysis completed.")

        except MeetingAnalysisError as error:
            st.session_state.analysis_result = None
            st.session_state.show_result = False
            st.error(str(error))


if (
    st.session_state.show_result
    and st.session_state.analysis_result
):
    
    render_result(st.session_state.analysis_result)


st.divider()
st.caption(
    "Responsible use: Review all AI-generated information before using it "
    "for official communication or project decisions."
)
