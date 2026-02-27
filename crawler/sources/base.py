from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class CrawledItem:
    title: str
    url: str
    source: str
    content_snippet: str = ""
    author: str = ""
    published_at: datetime = field(default_factory=datetime.utcnow)
    engagement: int = 0
    language: str = "en"
    keywords_matched: list = field(default_factory=list)


class BaseSource(ABC):
    @abstractmethod
    def fetch(self, keywords: list[str], since_hours: int = 72) -> list[CrawledItem]:
        pass
