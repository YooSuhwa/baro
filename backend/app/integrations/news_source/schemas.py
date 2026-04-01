from dataclasses import dataclass
from datetime import datetime


@dataclass
class RawArticle:
    title: str
    url: str
    content: str | None
    published_at: datetime | None
    source_name: str  # "naver" / "google"
