from data_classes.item import Item
from data_classes.resists import Resists
from data_classes.cut_rate import CutRate
from dataclasses import dataclass
from enum import Enum


class TypeEquip(Enum):
    HEADEQUIP = 'headEquip'
    BODYEQUIP = 'bodyEquip'
    ARMEQUIP = 'armEquip'
    LEGEQUIP = 'legEquip'


@dataclass(frozen=True, kw_only=True)
class Armor(Item):
    typeEquip: TypeEquip
    resists: Resists
    cutRate: CutRate
    balance: float



