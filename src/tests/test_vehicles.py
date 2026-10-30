from dataclasses import FrozenInstanceError
from datetime import date
import pytest

from carnet_entretien.models import Vehicle, Maintenance

TODAY = date(2026, 10, 30)


def test_is_new_vehicle_history_empty():
    my_sandero = Vehicle("Dacia", "Sandero", 40_000)

    assert my_sandero.maintenance_history == []


def test_vehicle_maintenance():
    maintenance = Maintenance("Entretien annuel", date(2026, 4, 19), 12_000)

    assert maintenance.maintenance_type == "Entretien annuel"
    assert maintenance.maintenance_date == date(2026, 4, 19)
    assert maintenance.mileage_km == 12_000


def test_vehicle_maintenance_immutability():
    maintenance = Maintenance("Entretien annuel", date(2026, 4, 19), 12_000)

    with pytest.raises(FrozenInstanceError):
        maintenance.maintenance_type = "Courroie de distribution"


def test_add_maintenance_to_vehicle():
    vehicle = Vehicle("Volskswagen", "Polo", 50_000)
    maintenance = Maintenance("Vidange", date(2026, 10, 1), 48_000)

    vehicle.add_maintenance(maintenance, TODAY)

    assert vehicle.maintenance_history == [maintenance]


def test_accept_maintenance_if_vehicle_and_maintenance_kms_are_equal():
    vehicle = Vehicle("Volskswagen", "Polo", 50_000)
    maintenance = Maintenance("Vidange", date(2026, 10, 1), 50_000)

    vehicle.add_maintenance(maintenance, TODAY)

    assert vehicle.maintenance_history == [maintenance]


def test_adding_second_maintenance_doesnt_eraise_the_older_one():
    vehicle = Vehicle("Volskswagen", "Polo", 50_000)
    old_maintenance = Maintenance("Vidange", date(2024, 10, 1), 12_000)
    new_maintenance = Maintenance("Vidange", date(2025, 10, 1), 24_000)

    vehicle.add_maintenance(old_maintenance, TODAY)
    vehicle.add_maintenance(new_maintenance, TODAY)

    assert vehicle.maintenance_history == [old_maintenance, new_maintenance]


def test_wrong_kms_raises_value_error():
    vehicle = Vehicle("Wolsksvagen", "Polo", 50_000)
    wrong_maintenance_kms = Maintenance("Vidange", date(2026, 10, 1), 60_000)

    with pytest.raises(
        ValueError,
        match="The maintenance kms must NOT be greather than the vehicle kms",
    ):
        vehicle.add_maintenance(wrong_maintenance_kms, TODAY)


def test_wrong_date_raises_value_error():
    vehicle = Vehicle("Wolsksvagen", "Polo", 50_000)
    wrong_maintenance_date = Maintenance("Vidange", date(2026, 11, 1), 48_000)

    with pytest.raises(
        ValueError, match="The maintenance date must NOT be greather than today's date"
    ):
        vehicle.add_maintenance(wrong_maintenance_date, TODAY)
