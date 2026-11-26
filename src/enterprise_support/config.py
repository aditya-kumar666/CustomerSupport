import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv


def create_chat_model() -> Any:
    env_file = Path(__file__).resolve().parents[2] / ".env"
    load_dotenv(env_file)

    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError("OpenAI support is not installed. Run: python -m pip install -e .") from exc

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    return OpenAIChatModel(
        client=OpenAI(api_key=api_key),
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    )


class OpenAIChatModel:
    def __init__(self, client: Any, model: str) -> None:
        self.client = client
        self.model = model

    def classify(self, complaint: str):
        from .classifier import SYSTEM_PROMPT
        from .models import ComplaintClassification

        schema = ComplaintClassification.model_json_schema()
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "ComplaintClassification",
                    "strict": True,
                    "schema": schema,
                },
            },
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": complaint},
            ],
        )
        content = response.choices[0].message.content
        if not content:
            raise ValueError("Model returned no classification content")
        return ComplaintClassification.model_validate_json(content)
