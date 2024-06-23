from dataclasses import dataclass


@dataclass
class Service:
    name: str
    internal_url: str
    slag: str
