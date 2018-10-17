from dataclasses import dataclass
from typing import Any, List

@dataclass
class Test:
    name: str
    duration: Any
    tags: List[str]
