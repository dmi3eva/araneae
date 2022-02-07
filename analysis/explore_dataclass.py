from dataclasses import dataclass, field
from typing import *


@dataclass
class Mention:
    db: Optional[str] = "Katya"
    details: List[str] = field(default_factory=lambda: [])


m = Mention()
t = m.details
s = ["a"] + m.details
a = 7