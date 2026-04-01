import json
import logging

from openai import AsyncOpenAI

from app.integrations.llm.prompts import SENTIMENT_PROMPT, SPEC_CHANGE_PROMPT
from app.integrations.llm.schemas import SentimentResult, SpecChangeDetection

logger = logging.getLogger(__name__)


class OpenAIProvider:
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model

    async def analyze_sentiment(self, title: str, content: str | None) -> SentimentResult:
        prompt = SENTIMENT_PROMPT.format(title=title, content=content or "(본문 없음)")

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                max_tokens=200,
                temperature=0.3,
            )
            result = json.loads(response.choices[0].message.content or "{}")
            sentiment = result.get("sentiment", "unknown")
            if sentiment not in ("positive", "negative", "neutral"):
                sentiment = "unknown"

            return SentimentResult(
                sentiment=sentiment,
                summary=result.get("summary", "")[:50],
            )
        except Exception as e:
            logger.error(f"OpenAI sentiment analysis failed: {e}")
            return SentimentResult(sentiment="unknown", summary="")

    async def detect_spec_changes(
        self, title: str, content: str | None, known_products: list[str]
    ) -> list[SpecChangeDetection]:
        if not known_products:
            return []

        prompt = SPEC_CHANGE_PROMPT.format(
            title=title,
            content=content or "(본문 없음)",
            products=", ".join(known_products),
        )

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                max_tokens=500,
                temperature=0.2,
            )
            raw = json.loads(response.choices[0].message.content or "[]")

            # Handle both {"changes": [...]} and direct [...] formats
            if isinstance(raw, dict):
                raw = raw.get("changes", raw.get("items", []))
            if not isinstance(raw, list):
                return []

            return [
                SpecChangeDetection(
                    product_name=item.get("product_name", ""),
                    field_name=item.get("field_name", ""),
                    old_value_hint=item.get("old_value_hint"),
                    new_value=item.get("new_value", ""),
                    source_quote=item.get("source_quote", ""),
                )
                for item in raw
                if item.get("product_name") and item.get("new_value")
            ]
        except Exception as e:
            logger.error(f"OpenAI spec change detection failed: {e}")
            return []
