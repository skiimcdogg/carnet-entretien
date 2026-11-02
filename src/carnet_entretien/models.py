from carnet_entretien.enums import maintenance_type

from dataclasses import dataclass, field
from datetime import date


@dataclass(frozen=True)
class Maintenance:
    maintenance_type: maintenance_type
    maintenance_date: date
    mileage_km: int


@dataclass
class Vehicle:
    brand: str
    model: str
    mileage_km: int
    maintenance_history: list[Maintenance] = field(default_factory=list)

    def add_maintenance(self, maintenance: Maintenance, today: date) -> None:
        if maintenance.mileage_km > self.mileage_km:
            raise ValueError(
                "The maintenance kms must NOT be greather than the vehicle kms"
            )
        if maintenance.maintenance_date > today:
            raise ValueError(
                "The maintenance date must NOT be greather than today's date"
            )

        self.maintenance_history.append(maintenance)
