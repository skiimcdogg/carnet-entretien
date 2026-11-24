from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from carnet_entretien.db.tables import MaintenanceRow, VehicleRow
from carnet_entretien.models import Maintenance, Vehicle


class SqlVehicleRepository:
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._session_factory = session_factory

    def save(self, vehicle_id: UUID, vehicle: Vehicle) -> None:
        with self._session_factory() as session:
            session.merge(_to_row(vehicle_id, vehicle))
            session.commit()

    def get(self, vehicle_id: UUID) -> Vehicle | None:
        with self._session_factory() as session:
            row = session.get(VehicleRow, vehicle_id)
            return None if row is None else _to_domain(row)

    def list_all(self) -> list[tuple[UUID, Vehicle]]:
        with self._session_factory() as session:
            rows = session.scalars(select(VehicleRow)).all()
            return [(row.id, _to_domain(row)) for row in rows]


def _to_row(vehicle_id: UUID, vehicle: Vehicle) -> VehicleRow:
    return VehicleRow(
        id=vehicle_id,
        brand=vehicle.brand,
        model=vehicle.model,
        mileage_kms=vehicle.mileage_kms,
        first_registration_date=vehicle.first_registration_date,
        maintenance_history=[
            MaintenanceRow(
                maintenance_type=m.maintenance_type, maintenance_date=m.maintenance_date, mileage_kms=m.mileage_kms
            )
            for m in vehicle.maintenance_history
        ],
    )


def _to_domain(vehicle_row: VehicleRow) -> Vehicle:
    return Vehicle(
        brand=vehicle_row.brand,
        model=vehicle_row.model,
        mileage_kms=vehicle_row.mileage_kms,
        first_registration_date=vehicle_row.first_registration_date,
        maintenance_history=[
            Maintenance(
                maintenance_type=m.maintenance_type, maintenance_date=m.maintenance_date, mileage_kms=m.mileage_kms
            )
            for m in vehicle_row.maintenance_history
        ],
    )
