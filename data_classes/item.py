from data_classes.base_item import BaseItem
from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class Item(BaseItem):
    weight: float
    sell_price: int
