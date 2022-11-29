from dataclasses import dataclass
from pydantic import BaseModel


@dataclass(frozen=True, kw_only=True)
class CutRate(BaseModel):
    neutralDamageCutRate: float
    slashDamageCutRate: float
    blowDamageCutRate: float
    thrustDamageCutRate: float
    magicDamageCutRate: float
    fireDamageCutRate: float
    thunderDamageCutRate: float
    darkDamageCutRate: float
    toughnessCorrectRate: float
