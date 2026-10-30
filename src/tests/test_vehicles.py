from dataclasses import FrozenInstanceError
from datetime import date
import pytest

from carnet_entretien.models import Vehicle, Maintenance


def test_is_new_vehicle_history_empty():
    my_sandero = Vehicle("Dacia", "Sandero", 40000)

    assert my_sandero.maintenance_history == []


def test_vehicle_maintenance():
    maintenance = Maintenance("Entretien annuel", date(2026, 4, 19), 12_000)

    with pytest.raises(FrozenInstanceError):
        maintenance.maintenance_type = "Courroie de distribution"

    assert maintenance.maintenance_type == "Entretien annuel"
    assert maintenance.maintenance_date == date(2026, 4, 19)
    assert maintenance.mileage_km == 12_000

def test_add_maintenance_to_vehicle():
    vehicle = Vehicle("Wolsksvagen", "Polo", 50_000)
    maintenance = Maintenance("Vidange", date(2026, 10, 1), 48_000)
    wrong_maintenance = Maintenance("Vidange", date(2026, 10, 1), 60_000)

    with pytest.raises(ValueError):
        vehicle.add_maintenance(wrong_maintenance, wrong_maintenance.maintenance_date)

    vehicle.add_maintenance(maintenance, date(2026, 10, 30))

    assert vehicle.maintenance_history[-1] == Maintenance("Vidange", date(2026, 10, 1), 48_000)

