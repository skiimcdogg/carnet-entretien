from carnet_entretien.repositories.base import VehicleRepository
from carnet_entretien.repositories.memory import InMemoryVehicleRepository

_repository = InMemoryVehicleRepository()


def get_vehicle_repository() -> VehicleRepository:
    return _repository
