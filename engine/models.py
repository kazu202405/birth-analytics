from dataclasses import dataclass, field
from datetime import date, time
from typing import Optional

@dataclass
class BirthData:
    birth_date: date
    birth_time: Optional[time] = None
    birth_place: Optional[str] = None
    name: Optional[str] = None
    gender: Optional[str] = None

    def __post_init__(self):
        if isinstance(self.birth_date, str):
            self.birth_date = date.fromisoformat(self.birth_date)
        if isinstance(self.birth_time, str):
            self.birth_time = time.fromisoformat(self.birth_time)
        if self.birth_date < date(1900, 1, 1) or self.birth_date > date(2100, 12, 31):
            raise ValueError("birth_date must be between 1900-01-01 and 2100-12-31")
        if self.gender and self.gender not in ("M", "F"):
            raise ValueError("gender must be 'M' or 'F'")

@dataclass
class DivinationResult:
    system_name: str
    system_id: str
    summary: str
    details: dict
    interpretation: str
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "system_name": self.system_name,
            "system_id": self.system_id,
            "summary": self.summary,
            "details": self.details,
            "interpretation": self.interpretation,
            "warnings": self.warnings,
        }
