from dataclasses import dataclass
from typing import Optional


@dataclass
class ScoreResult:
    criteria_key: str
    label: str
    weight: int
    partial_score: int
    weighted_score: float
    raw_value: str = ""
    note: str = ""