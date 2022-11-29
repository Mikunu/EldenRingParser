from dataclasses import dataclass
from pydantic import BaseModel


@dataclass(frozen=True, kw_only=True)
class Resists(BaseModel):
    resistPoison: float
    resistBlood: float
    resistFreeze: float
    resistCurse: float
    resistSleep: float
    resistMadness: float
