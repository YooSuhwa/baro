from dataclasses import dataclass


@dataclass
class PaginationParams:
    offset: int = 0
    limit: int = 20
