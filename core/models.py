from dataclasses import dataclass
from typing import Optional

@dataclass
class StrategyResult:
    success: bool
    technique: str
    message: str
    verify_url: Optional[str] = None
    status_code: Optional[int] = None
    filename: Optional[str] = None
    secret: Optional[str] = None
