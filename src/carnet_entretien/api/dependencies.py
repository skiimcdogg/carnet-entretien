from carnet_entretien.db.database import SessionLocal
from carnet_entretien.repositories.sql_vehicle_repository import SqlVehicleRepository
from carnet_entretien.repositories.vehicle_repository import VehicleRepository

_repository = SqlVehicleRepository(SessionLocal)


def get_vehicle_repository() -> VehicleRepository:
    return _repository
