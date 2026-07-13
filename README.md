# AI Meeting Intelligence Assistant

An AI-powered application that transforms meeting transcripts into structured summaries, decisions, action items, deadlines, risks, open questions, and follow-up communications.

## Project Objective

The objective of this project is to develop and evaluate an AI-assisted meeting organizer that converts unstructured meeting transcripts into clear and actionable information.

## Key Features

- Concise meeting summaries
- Decision extraction
- Action-item identification
- Owner and deadline detection
- Risk and blocker identification
- Open-question tracking
- Follow-up email generation
- Structured JSON output
- Simple Streamlit interface

## Why I Built This

This project applies practical AI skills from my Anthropic Claude learning, including:

- Prompt engineering
- Clear task delegation
- Structured output design
- Iterative refinement
- AI evaluation
- Responsible AI use
- Human review of generated results

## Project Structure

```text
ai-meeting-intelligence-assistant/
├── README.md
├── app.py
├── requirements.txt
├── prompts/
│   └── meeting_analysis_prompt.txt
├── sample_data/
│   └── meeting_01.txt
├── outputs/
│   └── sample_output.json
├── evaluation/
│   ├── rubric.md
│   └── evaluation_results.csv
└── screenshots/
```

## How to Run

1. Create and activate a virtual environment.
2. Install the dependencies:

```bash
pip install -r requirements.txt
```

3. Start the app:

```bash
streamlit run app.py
```

## Current Version

Version 1 is a local prototype. It uses a rule-based demo output so the interface can be tested without exposing an API key.

## Planned Improvements

- Connect the app to the Claude API
- Add TXT, DOCX, and PDF upload
- Export results to JSON and CSV
- Add evaluation across multiple meeting samples
- Improve deadline and owner extraction
- Add human-review and correction controls

## Responsible AI Notes

- The tool should not invent owners, deadlines, or decisions.
- Missing information should be marked as `Not specified`.
- Sensitive or confidential meeting transcripts should not be uploaded without permission.
- AI-generated summaries should be reviewed by a human before official use.
