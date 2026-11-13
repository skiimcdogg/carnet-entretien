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
    first_registration_date: date
    maintenance_history: list[Maintenance] = field(default_factory=list)

    def __post_init__(self) -> None:
        for maintenance in self.maintenance_history:
            self._check_mileage(maintenance)

    def _check_mileage(self, maintenance: Maintenance) -> None:
        if maintenance.mileage_kms > self.mileage_kms:
            raise ValueError("The maintenance kms must NOT be greater than the vehicle kms")

    def add_maintenance(self, maintenance: Maintenance, today: date) -> None:
        self._check_mileage(maintenance)

        if maintenance.maintenance_date > today:
            raise ValueError("The maintenance date must NOT be greater than today's date")

        self.maintenance_history.append(maintenance)

    def find_last_maintenance(self, maintenance_type: MaintenanceType) -> Maintenance | None:
        maintenance_list = [m for m in self.maintenance_history if m.maintenance_type is maintenance_type]

        return max(maintenance_list, key=lambda m: m.mileage_kms, default=None)

    def find_maintenance_to_do(
        self, plan: dict[MaintenanceType, MaintenanceRule], today: date
    ) -> list[MaintenanceType]:

        due_maintenance: list[MaintenanceType] = []

        for maintenance_type, rule in plan.items():
            last_maintenance = self.find_last_maintenance(maintenance_type)

            if last_maintenance is None:
                start_kms = 0
                start_date = self.first_registration_date
            else:
                start_kms = last_maintenance.mileage_kms
                start_date = last_maintenance.maintenance_date

            if (
                rule.kms is not None
                and (self.mileage_kms - start_kms) >= rule.kms
                or rule.months is not None
                and (today - start_date).days >= (rule.months * 30)
            ):
                due_maintenance.append(maintenance_type)

        return due_maintenance
