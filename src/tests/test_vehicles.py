from dataclasses import FrozenInstanceError
from datetime import date

import pytest

from carnet_entretien.enums import MaintenanceType
from carnet_entretien.models import Maintenance, Vehicle, MaintenanceRule

TODAY = date(2026, 10, 30)


def test_is_new_vehicle_history_empty():
    my_sandero = Vehicle("Dacia", "Sandero", 40_000)

    assert my_sandero.maintenance_history == []


def test_vehicle_maintenance():
    maintenance = Maintenance(MaintenanceType.ANNUAL_SERVICE, date(2026, 4, 19), 12_000)

    assert maintenance.maintenance_type == MaintenanceType.ANNUAL_SERVICE
    assert maintenance.maintenance_date == date(2026, 4, 19)
    assert maintenance.mileage_kms == 12_000


def test_vehicle_maintenance_immutability():
    maintenance = Maintenance(MaintenanceType.ANNUAL_SERVICE, date(2026, 4, 19), 12_000)

    with pytest.raises(FrozenInstanceError):
        maintenance.maintenance_type = MaintenanceType.BRAKE_PADS


def test_add_maintenance_to_vehicle():
    vehicle = Vehicle("Volskswagen", "Polo", 50_000)
    maintenance = Maintenance(MaintenanceType.ANNUAL_SERVICE, date(2026, 10, 1), 48_000)

    vehicle.add_maintenance(maintenance, TODAY)

    assert vehicle.maintenance_history == [maintenance]


def test_accept_maintenance_if_vehicle_and_maintenance_kms_are_equal():
    vehicle = Vehicle("Volskswagen", "Polo", 50_000)
    maintenance = Maintenance(MaintenanceType.ANNUAL_SERVICE, date(2026, 10, 1), 50_000)

    vehicle.add_maintenance(maintenance, TODAY)

    assert vehicle.maintenance_history == [maintenance]


def test_adding_second_maintenance_doesnt_erase_the_older_one():
    vehicle = Vehicle("Volskswagen", "Polo", 50_000)
    old_maintenance = Maintenance(
        MaintenanceType.ANNUAL_SERVICE, date(2024, 10, 1), 12_000
    )
    new_maintenance = Maintenance(
        MaintenanceType.ANNUAL_SERVICE, date(2025, 10, 1), 24_000
    )

    vehicle.add_maintenance(old_maintenance, TODAY)
    vehicle.add_maintenance(new_maintenance, TODAY)

    assert vehicle.maintenance_history == [old_maintenance, new_maintenance]


def test_wrong_kms_raises_value_error():
    vehicle = Vehicle("Volskswagen", "Polo", 50_000)
    wrong_maintenance_kms = Maintenance(
        MaintenanceType.ANNUAL_SERVICE, date(2026, 10, 1), 60_000
    )

    with pytest.raises(
        ValueError,
        match="The maintenance kms must NOT be greater than the vehicle kms",
    ):
        vehicle.add_maintenance(wrong_maintenance_kms, TODAY)


def test_wrong_date_raises_value_error():
    vehicle = Vehicle("Volskswagen", "Polo", 50_000)
    wrong_maintenance_date = Maintenance(
        MaintenanceType.ANNUAL_SERVICE, date(2026, 11, 1), 48_000
    )

    with pytest.raises(
        ValueError, match="The maintenance date must NOT be greater than today's date"
    ):
        vehicle.add_maintenance(wrong_maintenance_date, TODAY)


def test_get_last_maintenance_type_return_none_if_not_exist():
    vehicle = Vehicle(
        "Volskswagen",
        "Polo",
        50_000,
        [Maintenance(MaintenanceType.ANNUAL_SERVICE, date(2025, 10, 1), 24_000)],
    )

    last_maintenance = vehicle.find_last_maintenance(MaintenanceType.TRANSMISSION)

    assert last_maintenance is None


def test_get_last_maintenance_when_there_is_just_one():
    vehicle = Vehicle(
        "Volskswagen",
        "Polo",
        50_000,
        [Maintenance(MaintenanceType.ANNUAL_SERVICE, date(2025, 10, 1), 24_000)],
    )

    last_maintenance = vehicle.find_last_maintenance(MaintenanceType.ANNUAL_SERVICE)

    assert last_maintenance == Maintenance(
        MaintenanceType.ANNUAL_SERVICE, date(2025, 10, 1), 24_000
    )


def test_get_last_maintenance_when_there_is_two_of_the_same_type():
    vehicle = Vehicle(
        "Volskswagen",
        "Polo",
        50_000,
        [
            Maintenance(MaintenanceType.ANNUAL_SERVICE, date(2026, 10, 1), 36_000),
            Maintenance(MaintenanceType.ANNUAL_SERVICE, date(2025, 10, 1), 24_000),
        ],
    )

    last_maintenance = vehicle.find_last_maintenance(MaintenanceType.ANNUAL_SERVICE)

    assert last_maintenance == Maintenance(
        MaintenanceType.ANNUAL_SERVICE, date(2026, 10, 1), 36_000
    )


def test_rule_with_only_kms_is_accepted():
    rule = MaintenanceRule(kms=120_000)

    assert rule.kms == 120_000
    assert rule.months is None


def test_rule_with_only_months_is_accepted():
    rule = MaintenanceRule(months=12)

    assert rule.kms is None
    assert rule.months == 12


def test_rule_with_neither_kms_or_months_is_refused():

    with pytest.raises(ValueError, match="Kms or months must have a value"):
        MaintenanceRule()
