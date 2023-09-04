from dataclasses import dataclass, asdict


@dataclass
class QueryParams:
    location: str
    distance: int
    limit: int

    def dict(self):
        return asdict(self)
