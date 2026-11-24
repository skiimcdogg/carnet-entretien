from datetime import date
from uuid import uuid4

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from carnet_entretien.db.tables import Base
from carnet_entretien.enums import MaintenanceType
from carnet_entretien.models import Maintenance, Vehicle
from carnet_entretien.repositories.in_memory_vehicle_repository import InMemoryVehicleRepository
from carnet_entretien.repositories.sql_vehicle_repository import SqlVehicleRepository
from carnet_entretien.repositories.vehicle_repository import VehicleRepository

REGISTRATION_DATE = date(2010, 10, 30)


@pytest.fixture(params=["memory", "sql"])
def repository(request) -> VehicleRepository:
    if request.param == "memory":
        return InMemoryVehicleRepository()

    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    return SqlVehicleRepository(sessionmaker(engine))


@pytest.fixture
def vehicle() -> Vehicle:
    return Vehicle("Dacia", "Sandero", 40_000, REGISTRATION_DATE)


def test_saved_vehicle_can_be_found(repository, vehicle):
    vehicle_id = uuid4()

    repository.save(vehicle_id, vehicle)

    assert repository.get(vehicle_id) == vehicle


def test_get_vehicle_with_unknown_id_returns_none(repository):
    assert repository.get(uuid4()) is None


def test_list_all_returns_all_vehicles_with_its_id(repository, vehicle):
    first_id, second_id = uuid4(), uuid4()

    second_vehicle = Vehicle("Dacia", "Sandero", 45_000, REGISTRATION_DATE)

    repository.save(first_id, vehicle)
    repository.save(second_id, second_vehicle)
    vehicle_list = repository.list_all()

    assert len(vehicle_list) == 2
    assert (first_id, vehicle) in vehicle_list
    assert (second_id, second_vehicle) in vehicle_list


def test_vehicle_with_maintenance(repository, vehicle):
    vehicle.maintenance_history = [
        Maintenance(MaintenanceType.ANNUAL_SERVICE, date(2022, 6, 1), 38_000),
        Maintenance(MaintenanceType.ANNUAL_SERVICE, date(2021, 6, 1), 26_000),
    ]

    vehicle_id = uuid4()
    repository.save(vehicle_id, vehicle)
    vehicle_response = repository.get(vehicle_id)

    assert vehicle_response == Vehicle(
        "Dacia",
        "Sandero",
        40_000,
        REGISTRATION_DATE,
        [
            Maintenance(MaintenanceType.ANNUAL_SERVICE, date(2022, 6, 1), 38_000),
            Maintenance(MaintenanceType.ANNUAL_SERVICE, date(2021, 6, 1), 26_000),
        ],
    )
