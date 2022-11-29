from dataclasses import dataclass
from pydantic import BaseModel


@dataclass(frozen=True, kw_only=True)
class Resists(BaseModel):
    resist_poison: int
    resist_blood: int
    resist_freeze: int
    resist_curse: int
    resist_sleep: int
    resist_madness: int

