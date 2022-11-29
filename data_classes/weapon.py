from data_classes.item import Item
from data_classes.cut_rate import CutRate
from data_classes.stat_requirements import StatRequirements
from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class AttackStats:
    attackBasePhysics: int
    attackBaseMagic: int
    attackBaseFire: int
    attackBaseThunder: int
    attackBaseDark: int
    throwAtkRate: int


@dataclass(frozen=True, kw_only=True)
class Weapon(Item):
    stat_requirements: StatRequirements
    attack_damage: AttackStats
    cut_rate: CutRate
    balance: float
