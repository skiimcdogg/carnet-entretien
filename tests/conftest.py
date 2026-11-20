import pytest
from fastapi.testclient import TestClient

from carnet_entretien.api.dependencies import get_vehicle_repository
from carnet_entretien.api.main import app
from carnet_entretien.repositories.memory import InMemoryVehicleRepository


@pytest.fixture
def client():
    repository = InMemoryVehicleRepository()
    app.dependency_overrides[get_vehicle_repository] = lambda: repository
    yield TestClient(app)
    app.dependency_overrides.clear()
