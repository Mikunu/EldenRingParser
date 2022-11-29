from data_classes.base_item import BaseItem
from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class SwordArt(BaseItem):
    fp_cost: float
