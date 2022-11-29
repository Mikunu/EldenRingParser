from data_classes.item import Item
from data_classes.cut_rate import CutRate
from data_classes.stat_requirements import StatRequirements
from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class AttackStats:
    attack_base_physics: int
    attack_base_magic: int
    attack_base_fire: int
    attack_base_thunder: int
    attack_base_dark: int
    throw_atk_rate: int


@dataclass(frozen=True, kw_only=True)
class Weapon(Item):
    stat_requirements: StatRequirements
    attack_damage: AttackStats
    cut_rate: CutRate
    balance: float
