from typing import Protocol

from app.integrations.news_source.schemas import RawArticle


class NewsSourceCollector(Protocol):
    @property
    def source_name(self) -> str: ...

    async def search(self, keyword: str, max_results: int = 10) -> list[RawArticle]: ...
