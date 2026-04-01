from typing import Protocol

from app.integrations.llm.schemas import SentimentResult, SpecChangeDetection


class LLMProvider(Protocol):
    async def analyze_sentiment(self, title: str, content: str | None) -> SentimentResult: ...

    async def detect_spec_changes(
        self, title: str, content: str | None, known_products: list[str]
    ) -> list[SpecChangeDetection]: ...
