from dataclasses import dataclass, field
from datetime import date


@dataclass(frozen=True)
class Maintenance:
    maintenance_type: str
    maintenance_date: date
    mileage_km: int


@dataclass
class Vehicle:
    brand: str
    model: str
    mileage_km: int
    maintenance_history: list[Maintenance] = field(default_factory=list)

    def add_maintenance(self, maintenance: Maintenance, today: date) -> None:
        if maintenance.mileage_km > self.mileage_km or maintenance.maintenance_date > today:
            raise ValueError("The maintenance km or date cannot be superior to the vehicle")

        self.maintenance_history.append(maintenance)
