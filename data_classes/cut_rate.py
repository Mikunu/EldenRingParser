from dataclasses import dataclass
from pydantic import BaseModel


@dataclass(frozen=True, kw_only=True)
class CutRate(BaseModel):
    neutral_damage_cut_rate: float
    slash_damage_cut_rate: float
    blow_damage_cut_rate: float
    thrust_damage_cut_rate: float
    magic_damage_cut_rate: float
    fire_damage_cut_rate: float
    thunder_damage_cut_rate: float
    dark_damage_cut_rate: float
    toughness_correct_rate: float

