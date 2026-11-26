# Enterprise Customer Support Agent

## Day 1: Complaint Classification Agent

The classifier is a LangGraph state machine. The OpenAI model call is isolated behind a small structured-chat interface.

Classify a customer complaint into a structured Pydantic result.

### Setup

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
copy .env.example .env
```

The app loads `.env` from the project root. Set `OPENAI_API_KEY` there; optionally set `OPENAI_MODEL`.

### Run

```powershell
python -m enterprise_support.classify "My payment was deducted twice, but I received only one order."
pytest
```
