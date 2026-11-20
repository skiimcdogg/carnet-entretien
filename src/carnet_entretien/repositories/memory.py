from uuid import UUID

from carnet_entretien.models import Vehicle


class InMemoryVehicleRepository:
    def __init__(self) -> None:
        self._vehicles: dict[UUID, Vehicle] = {}

    def save(self, vehicle_id: UUID, vehicle: Vehicle) -> None:
        self._vehicles[vehicle_id] = vehicle

    def get(self, vehicle_id: UUID) -> Vehicle | None:
        return self._vehicles.get(vehicle_id)

    def list_all(self) -> list[tuple[UUID, Vehicle]]:
        return list(self._vehicles.items())
