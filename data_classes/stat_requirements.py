from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class PhysicalRequirements:
    requirement_strength: int
    requirement_agility: int


@dataclass(frozen=True, kw_only=True)
class MagicRequirements:
    requirement_magic: int
    requirement_faith: int
    requirement_luck: int


@dataclass(frozen=True, kw_only=True)
class StatRequirements(PhysicalRequirements, MagicRequirements):
    pass
