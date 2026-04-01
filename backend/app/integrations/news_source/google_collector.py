import logging

import httpx

from app.integrations.news_source.schemas import RawArticle

logger = logging.getLogger(__name__)


class GoogleNewsCollector:
    """Google Custom Search JSON API collector."""

    SEARCH_URL = "https://www.googleapis.com/customsearch/v1"

    def __init__(self, api_key: str, cse_id: str):
        self.api_key = api_key
        self.cse_id = cse_id

    @property
    def source_name(self) -> str:
        return "google"

    async def search(self, keyword: str, max_results: int = 10) -> list[RawArticle]:
        if not self.api_key or not self.cse_id:
            logger.warning("Google API credentials not configured, skipping")
            return []

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    self.SEARCH_URL,
                    params={
                        "key": self.api_key,
                        "cx": self.cse_id,
                        "q": keyword,
                        "num": min(max_results, 10),
                        "sort": "date",
                    },
                )
                response.raise_for_status()
                data = response.json()

            articles = []
            for item in data.get("items", []):
                title = item.get("title", "")
                url = item.get("link", "")
                snippet = item.get("snippet", "")

                if title and url:
                    articles.append(
                        RawArticle(
                            title=title,
                            url=url,
                            content=snippet,
                            published_at=None,
                            source_name="google",
                        )
                    )

            logger.info(f"Google: collected {len(articles)} articles for keyword '{keyword}'")
            return articles

        except httpx.HTTPError as e:
            logger.error(f"Google API error for keyword '{keyword}': {e}")
            return []
        except Exception as e:
            logger.error(f"Google collector unexpected error: {e}")
            return []
