from data_classes.base_item import BaseItem
from data_classes.stat_requirements import StatRequirements
from dataclasses import dataclass
from enum import Enum


class TypeSchool(Enum):
    MAGIC = 'Магия'
    PRAYER = 'Молитва'


@dataclass(frozen=True, kw_only=True)
class Magic(BaseItem):
    type_school: TypeSchool
    fp_cost: int
    stamina_cost: int
    slots_used: int
    effectEndurance: float
    stat_requirements: StatRequirements

