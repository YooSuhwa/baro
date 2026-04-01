import logging
import re
from datetime import datetime

import httpx

from app.integrations.news_source.schemas import RawArticle

logger = logging.getLogger(__name__)


class NaverNewsCollector:
    """Naver Search News API collector."""

    SEARCH_URL = "https://openapi.naver.com/v1/search/news.json"

    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret

    @property
    def source_name(self) -> str:
        return "naver"

    async def search(self, keyword: str, max_results: int = 10) -> list[RawArticle]:
        if not self.client_id or not self.client_secret:
            logger.warning("Naver API credentials not configured, skipping")
            return []

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    self.SEARCH_URL,
                    params={"query": keyword, "display": max_results, "sort": "date"},
                    headers={
                        "X-Naver-Client-Id": self.client_id,
                        "X-Naver-Client-Secret": self.client_secret,
                    },
                )
                response.raise_for_status()
                data = response.json()

            articles = []
            for item in data.get("items", []):
                title = self._strip_html(item.get("title", ""))
                description = self._strip_html(item.get("description", ""))
                url = item.get("originallink") or item.get("link", "")
                pub_date = self._parse_date(item.get("pubDate", ""))

                if title and url:
                    articles.append(
                        RawArticle(
                            title=title,
                            url=url,
                            content=description,
                            published_at=pub_date,
                            source_name="naver",
                        )
                    )

            logger.info(f"Naver: collected {len(articles)} articles for keyword '{keyword}'")
            return articles

        except httpx.HTTPError as e:
            logger.error(f"Naver API error for keyword '{keyword}': {e}")
            return []
        except Exception as e:
            logger.error(f"Naver collector unexpected error: {e}")
            return []

    @staticmethod
    def _strip_html(text: str) -> str:
        return re.sub(r"<[^>]+>", "", text).strip()

    @staticmethod
    def _parse_date(date_str: str) -> datetime | None:
        try:
            from email.utils import parsedate_to_datetime

            return parsedate_to_datetime(date_str)
        except Exception:
            return None
