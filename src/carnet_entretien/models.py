from dataclasses import dataclass, field
from datetime import date

from carnet_entretien.enums import MaintenanceType


@dataclass(frozen=True)
class Maintenance:
    maintenance_type: MaintenanceType
    maintenance_date: date
    mileage_kms: int


@dataclass(frozen=True)
class MaintenanceRule:
    kms: int | None = None
    months: int | None = None

    def __post_init__(self) -> None:
        if self.kms is None and self.months is None:
            raise ValueError("Kms or months must have a value")


@dataclass
class Vehicle:
    brand: str
    model: str
    mileage_kms: int
    maintenance_history: list[Maintenance] = field(default_factory=list)

    def add_maintenance(self, maintenance: Maintenance, today: date) -> None:
        if maintenance.mileage_kms > self.mileage_kms:
            raise ValueError(
                "The maintenance kms must NOT be greater than the vehicle kms"
            )
        if maintenance.maintenance_date > today:
            raise ValueError(
                "The maintenance date must NOT be greater than today's date"
            )

        self.maintenance_history.append(maintenance)

    def find_last_maintenance(
        self, maintenance_type: MaintenanceType
    ) -> Maintenance | None:
        maintenance_list = [
            m
            for m in self.maintenance_history
            if m.maintenance_type is maintenance_type
        ]

        return max(maintenance_list, key=lambda m: m.mileage_kms, default=None)
