import json
import os
from pathlib import Path
from typing import Any

from anthropic import Anthropic
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
PROMPT_PATH = BASE_DIR / "prompts" / "meeting_analysis_prompt.txt"

load_dotenv()


class MeetingAnalysisError(Exception):
    """Raised when Claude cannot return a usable meeting analysis."""


def load_prompt_template() -> str:
    """Load the meeting-analysis prompt from disk."""
    try:
        return PROMPT_PATH.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise MeetingAnalysisError(
            "The meeting-analysis prompt file was not found."
        ) from exc


def extract_json(text: str) -> dict[str, Any]:
    """
    Convert Claude's response into a Python dictionary.

    This also handles responses wrapped in Markdown code fences.
    """
    cleaned = text.strip()

    if cleaned.startswith("```"):
        cleaned = cleaned.removeprefix("```json")
        cleaned = cleaned.removeprefix("```")
        cleaned = cleaned.removesuffix("```")
        cleaned = cleaned.strip()

    try:
        result = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise MeetingAnalysisError(
            "Claude returned an invalid JSON response."
        ) from exc

    if not isinstance(result, dict):
        raise MeetingAnalysisError(
            "Claude's response did not contain a JSON object."
        )

    return result


def validate_result(result: dict[str, Any]) -> dict[str, Any]:
    """Confirm that the required output fields exist."""
    required_fields = {
        "meeting_summary",
        "key_decisions",
        "action_items",
        "risks_or_blockers",
        "open_questions",
        "follow_up_email",
    }

    missing_fields = required_fields - result.keys()

    if missing_fields:
        missing = ", ".join(sorted(missing_fields))
        raise MeetingAnalysisError(
            f"Claude's response is missing required fields: {missing}"
        )

    if not isinstance(result["key_decisions"], list):
        raise MeetingAnalysisError(
            "The key_decisions field must be a list."
        )

    if not isinstance(result["action_items"], list):
        raise MeetingAnalysisError(
            "The action_items field must be a list."
        )

    return result


def analyze_meeting(transcript: str) -> dict[str, Any]:
    """Send a transcript to Claude and return structured meeting analysis."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    model = os.getenv("CLAUDE_MODEL", "claude-haiku-4-5")

    if not api_key:
        raise MeetingAnalysisError(
            "ANTHROPIC_API_KEY was not found. Add it to your .env file."
        )

    if not transcript.strip():
        raise MeetingAnalysisError(
            "The meeting transcript cannot be empty."
        )

    prompt_template = load_prompt_template()
    user_prompt = prompt_template.replace(
        "{{TRANSCRIPT}}",
        transcript.strip(),
    )

    client = Anthropic(api_key=api_key)

    try:
        response = client.messages.create(
            model=model,
            max_tokens=1200,
            temperature=0,
            messages=[
                {
                    "role": "user",
                    "content": user_prompt,
                }
            ],
        )
    except Exception as exc:
        raise MeetingAnalysisError(
            f"Claude API request failed: {exc}"
        ) from exc

    text_parts = [
        block.text
        for block in response.content
        if getattr(block, "type", None) == "text"
    ]

    if not text_parts:
        raise MeetingAnalysisError(
            "Claude returned no text response."
        )

    result = extract_json("\n".join(text_parts))
    return validate_result(result)