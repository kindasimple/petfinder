from dataclasses import asdict, dataclass


@dataclass
class QueryParams:
    location: str
    distance: int
    limit: int

    def dict(self):
        return asdict(self)
