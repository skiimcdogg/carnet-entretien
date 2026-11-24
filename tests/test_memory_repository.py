from datetime import date
from uuid import uuid4

import pytest

from carnet_entretien.models import Vehicle
from carnet_entretien.repositories.in_memory_vehicle_repository import InMemoryVehicleRepository

REGISTRATION_DATE = date(2010, 10, 30)


@pytest.fixture
def repository() -> InMemoryVehicleRepository:
    return InMemoryVehicleRepository()


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

    assert repository.list_all() == [(first_id, vehicle), (second_id, second_vehicle)]
