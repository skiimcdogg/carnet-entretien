from carnet_entretien.repositories.in_memory_vehicle_repository import InMemoryVehicleRepository
from carnet_entretien.repositories.vehicle_repository import VehicleRepository

_repository = InMemoryVehicleRepository()


def get_vehicle_repository() -> VehicleRepository:
    return _repository
