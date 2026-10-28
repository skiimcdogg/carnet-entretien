from dataclasses import dataclass, field
from datetime import date


@dataclass(frozen=True)
class Maintenance:
    maintenance_type: str
    maintanance_date: date
    mileage_km: int


@dataclass
class Vehicle:
    brand: str
    model: str
    mileage_km: int
    maintenance_history: list[Maintenance] = field(default_factory=list)
