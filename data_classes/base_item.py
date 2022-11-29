from dataclasses import dataclass
from pydantic import BaseModel


@dataclass(frozen=True, kw_only=True)
class BaseItem(BaseModel):
    name: str
    en_name: str
    caption: str
