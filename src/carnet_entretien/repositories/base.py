from typing import Protocol
from uuid import UUID

from carnet_entretien.models import Vehicle


class VehicleRepository(Protocol):
    def save(self, vehicle_id: UUID, vehicle: Vehicle) -> None: ...
    def get(self, vehicle_id: UUID) -> Vehicle | None: ...
    def list_all(self) -> list[tuple[UUID, Vehicle]]: ...
