from dataclasses import dataclass


@dataclass
class SentimentResult:
    sentiment: str  # positive / negative / neutral / unknown
    summary: str  # max 50 chars


@dataclass
class SpecChangeDetection:
    product_name: str
    field_name: str
    old_value_hint: str | None
    new_value: str
    source_quote: str
