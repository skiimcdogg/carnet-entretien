from dataclasses import FrozenInstanceError
from datetime import date

import pytest

from carnet_entretien.enums import MaintenanceType
from carnet_entretien.models import Maintenance, MaintenanceRule, Vehicle

TODAY = date(2026, 11, 10)
REGISTRATION_DATE = date(2010, 10, 30)


def test_is_new_vehicle_history_empty():
    my_sandero = Vehicle("Dacia", "Sandero", 40_000, REGISTRATION_DATE)

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
    vehicle = Vehicle("Volkswagen", "Polo", 50_000, REGISTRATION_DATE)
    maintenance = Maintenance(MaintenanceType.ANNUAL_SERVICE, date(2026, 10, 1), 48_000)

    vehicle.add_maintenance(maintenance, TODAY)

    assert vehicle.maintenance_history == [maintenance]


def test_accept_maintenance_if_vehicle_and_maintenance_kms_are_equal():
    vehicle = Vehicle("Volkswagen", "Polo", 50_000, REGISTRATION_DATE)
    maintenance = Maintenance(MaintenanceType.ANNUAL_SERVICE, date(2026, 10, 1), 50_000)

    vehicle.add_maintenance(maintenance, TODAY)

    assert vehicle.maintenance_history == [maintenance]


def test_adding_second_maintenance_doesnt_erase_the_older_one():
    vehicle = Vehicle("Volkswagen", "Polo", 50_000, REGISTRATION_DATE)
    old_maintenance = Maintenance(MaintenanceType.ANNUAL_SERVICE, date(2024, 10, 1), 12_000)
    new_maintenance = Maintenance(MaintenanceType.ANNUAL_SERVICE, date(2025, 10, 1), 24_000)

    vehicle.add_maintenance(old_maintenance, TODAY)
    vehicle.add_maintenance(new_maintenance, TODAY)

    assert vehicle.maintenance_history == [old_maintenance, new_maintenance]


def test_wrong_kms_raises_value_error():
    vehicle = Vehicle("Volkswagen", "Polo", 50_000, REGISTRATION_DATE)
    wrong_maintenance_kms = Maintenance(MaintenanceType.ANNUAL_SERVICE, date(2026, 10, 1), 60_000)

    with pytest.raises(
        ValueError,
        match="The maintenance kms must NOT be greater than the vehicle kms",
    ):
        vehicle.add_maintenance(wrong_maintenance_kms, TODAY)


def test_wrong_date_raises_value_error():
    vehicle = Vehicle("Volkswagen", "Polo", 50_000, REGISTRATION_DATE)
    wrong_maintenance_date = Maintenance(MaintenanceType.ANNUAL_SERVICE, date(2026, 11, 1), 48_000)

    with pytest.raises(ValueError, match="The maintenance date must NOT be greater than today's date"):
        vehicle.add_maintenance(wrong_maintenance_date, date(2026, 10, 30))


def test_get_last_maintenance_type_return_none_if_not_exist():
    vehicle = Vehicle(
        "Volkswagen",
        "Polo",
        50_000,
        REGISTRATION_DATE,
        [Maintenance(MaintenanceType.ANNUAL_SERVICE, date(2025, 10, 1), 24_000)],
    )

    last_maintenance = vehicle.find_last_maintenance(MaintenanceType.TRANSMISSION)

    assert last_maintenance is None


def test_get_last_maintenance_when_there_is_just_one():
    vehicle = Vehicle(
        "Volkswagen",
        "Polo",
        50_000,
        REGISTRATION_DATE,
        [Maintenance(MaintenanceType.ANNUAL_SERVICE, date(2025, 10, 1), 24_000)],
    )

    last_maintenance = vehicle.find_last_maintenance(MaintenanceType.ANNUAL_SERVICE)

    assert last_maintenance == Maintenance(MaintenanceType.ANNUAL_SERVICE, date(2025, 10, 1), 24_000)


def test_get_last_maintenance_when_there_is_two_of_the_same_type():
    vehicle = Vehicle(
        "Volkswagen",
        "Polo",
        50_000,
        REGISTRATION_DATE,
        [
            Maintenance(MaintenanceType.ANNUAL_SERVICE, date(2026, 10, 1), 36_000),
            Maintenance(MaintenanceType.ANNUAL_SERVICE, date(2025, 10, 1), 24_000),
        ],
    )

    last_maintenance = vehicle.find_last_maintenance(MaintenanceType.ANNUAL_SERVICE)

    assert last_maintenance == Maintenance(MaintenanceType.ANNUAL_SERVICE, date(2026, 10, 1), 36_000)


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


def test_maintenance_is_due_if_kms_are_reached():
    maintenance_plan = {MaintenanceType.ANNUAL_SERVICE: MaintenanceRule(kms=15_000, months=12)}
    vehicle = Vehicle(
        "Volkswagen",
        "Polo",
        70_000,
        REGISTRATION_DATE,
        [
            Maintenance(MaintenanceType.ANNUAL_SERVICE, date(2026, 8, 28), 50_000),
        ],
    )

    due_maintenance: list[MaintenanceType] = vehicle.find_maintenance_to_do(maintenance_plan, TODAY)

    assert due_maintenance == [MaintenanceType.ANNUAL_SERVICE]


def test_maintenance_is_due_if_date_is_reached():
    maintenance_plan = {MaintenanceType.ANNUAL_SERVICE: MaintenanceRule(kms=15_000, months=12)}
    vehicle = Vehicle(
        "Volkswagen",
        "Polo",
        52_000,
        REGISTRATION_DATE,
        [
            Maintenance(MaintenanceType.ANNUAL_SERVICE, date(2025, 11, 10), 40_000),
        ],
    )

    due_maintenance: list[MaintenanceType] = vehicle.find_maintenance_to_do(maintenance_plan, TODAY)

    assert due_maintenance == [MaintenanceType.ANNUAL_SERVICE]


def test_maintenance_is_not_due_if_neither_date_or_kms_are_reached():
    maintenance_plan = {MaintenanceType.ANNUAL_SERVICE: MaintenanceRule(kms=15_000, months=12)}
    vehicle = Vehicle(
        "Volkswagen",
        "Polo",
        55_000,
        REGISTRATION_DATE,
        [
            Maintenance(MaintenanceType.ANNUAL_SERVICE, date(2026, 6, 10), 50_000),
        ],
    )

    due_maintenance: list[MaintenanceType] = vehicle.find_maintenance_to_do(maintenance_plan, TODAY)

    assert due_maintenance == []


def test_maintenance_is_due_if_no_maintenance_was_ever_made():
    maintenance_plan = {MaintenanceType.ANNUAL_SERVICE: MaintenanceRule(kms=15_000, months=12)}
    vehicle = Vehicle(
        "Volkswagen",
        "Polo",
        55_000,
        REGISTRATION_DATE,
    )

    due_maintenance: list[MaintenanceType] = vehicle.find_maintenance_to_do(maintenance_plan, TODAY)

    assert due_maintenance == [MaintenanceType.ANNUAL_SERVICE]


def test_maintenance_is_not_due_if_new_vehicle():
    maintenance_plan = {MaintenanceType.ANNUAL_SERVICE: MaintenanceRule(kms=15_000, months=12)}
    vehicle = Vehicle(
        "Volkswagen",
        "Polo",
        5_000,
        date(2026, 6, 1),
    )

    due_maintenance: list[MaintenanceType] = vehicle.find_maintenance_to_do(maintenance_plan, TODAY)

    assert due_maintenance == []


def test_maintenance_is_due_if_new_vehicle_with_one_year_old():
    maintenance_plan = {MaintenanceType.ANNUAL_SERVICE: MaintenanceRule(kms=15_000, months=12)}
    vehicle = Vehicle(
        "Volkswagen",
        "Polo",
        5_000,
        date(2025, 6, 1),
    )

    due_maintenance: list[MaintenanceType] = vehicle.find_maintenance_to_do(maintenance_plan, TODAY)

    assert due_maintenance == [MaintenanceType.ANNUAL_SERVICE]


def test_maintenance_is_due_if_kms_are_equals_to_the_limit():
    maintenance_plan = {MaintenanceType.ANNUAL_SERVICE: MaintenanceRule(kms=15_000, months=12)}
    vehicle = Vehicle(
        "Volkswagen",
        "Polo",
        65_000,
        REGISTRATION_DATE,
        [
            Maintenance(MaintenanceType.ANNUAL_SERVICE, date(2026, 6, 10), 50_000),
        ],
    )

    due_maintenance: list[MaintenanceType] = vehicle.find_maintenance_to_do(maintenance_plan, TODAY)

    assert due_maintenance == [MaintenanceType.ANNUAL_SERVICE]


def test_last_maintenance_is_taken_and_not_due():
    maintenance_plan = {MaintenanceType.ANNUAL_SERVICE: MaintenanceRule(kms=15_000, months=12)}
    vehicle = Vehicle(
        "Volkswagen",
        "Polo",
        70_000,
        REGISTRATION_DATE,
        [
            Maintenance(MaintenanceType.ANNUAL_SERVICE, date(2025, 6, 10), 50_000),
            Maintenance(MaintenanceType.ANNUAL_SERVICE, date(2026, 8, 28), 60_000),
        ],
    )

    due_maintenance: list[MaintenanceType] = vehicle.find_maintenance_to_do(maintenance_plan, TODAY)

    assert due_maintenance == []


def test_two_maintenances_in_plan_and_one_is_due():
    maintenance_plan = {
        MaintenanceType.ANNUAL_SERVICE: MaintenanceRule(kms=15_000, months=12),
        MaintenanceType.TIMING_BELT: MaintenanceRule(kms=120_000, months=60),
    }
    vehicle = Vehicle(
        "Volkswagen",
        "Polo",
        70_000,
        REGISTRATION_DATE,
        [
            Maintenance(MaintenanceType.ANNUAL_SERVICE, date(2026, 8, 28), 50_000),
            Maintenance(MaintenanceType.TIMING_BELT, date(2024, 8, 28), 20_000),
        ],
    )

    due_maintenance: list[MaintenanceType] = vehicle.find_maintenance_to_do(maintenance_plan, TODAY)

    assert due_maintenance == [MaintenanceType.ANNUAL_SERVICE]


def test_brake_pads_not_due_with_no_limit_date():
    maintenance_plan = {
        MaintenanceType.BRAKE_PADS: MaintenanceRule(kms=40_000),
    }
    vehicle = Vehicle(
        "Volkswagen",
        "Polo",
        50_000,
        REGISTRATION_DATE,
        [
            Maintenance(MaintenanceType.BRAKE_PADS, date(2020, 8, 28), 20_000),
        ],
    )

    due_maintenance: list[MaintenanceType] = vehicle.find_maintenance_to_do(maintenance_plan, TODAY)

    assert due_maintenance == []


def test_ac_recharge_has_no_kms_limit_and_is_not_due():
    maintenance_plan = {
        MaintenanceType.AC_RECHARGE: MaintenanceRule(months=24),
    }
    vehicle = Vehicle(
        "Volkswagen",
        "Polo",
        200_000,
        REGISTRATION_DATE,
        [
            Maintenance(MaintenanceType.AC_RECHARGE, date(2026, 6, 28), 20_000),
        ],
    )

    due_maintenance: list[MaintenanceType] = vehicle.find_maintenance_to_do(maintenance_plan, TODAY)

    assert due_maintenance == []


def test_ac_recharge_has_no_kms_limit_and_is_due():
    maintenance_plan = {
        MaintenanceType.AC_RECHARGE: MaintenanceRule(months=24),
    }
    vehicle = Vehicle(
        "Volkswagen",
        "Polo",
        50_000,
        REGISTRATION_DATE,
        [
            Maintenance(MaintenanceType.AC_RECHARGE, date(2024, 6, 1), 48_000),
        ],
    )

    due_maintenance: list[MaintenanceType] = vehicle.find_maintenance_to_do(maintenance_plan, TODAY)

    assert due_maintenance == [MaintenanceType.AC_RECHARGE]


def test_vehicle_maintenance_with_wrong_kms_raise_value_error():

    with pytest.raises(ValueError, match="The maintenance kms must NOT be greater than the vehicle kms"):
        Vehicle(
            "Volkswagen",
            "Polo",
            50_000,
            REGISTRATION_DATE,
            [
                Maintenance(MaintenanceType.ANNUAL_SERVICE, date(2023, 6, 1), 60_000),
                Maintenance(MaintenanceType.ANNUAL_SERVICE, date(2022, 6, 1), 48_000),
                Maintenance(MaintenanceType.ANNUAL_SERVICE, date(2021, 6, 1), 36_000),
            ],
        )


def test_vehicle_with_negative_kms_raise_error():
    with pytest.raises(ValueError, match="Kms cannot be lower than zero"):
        Vehicle(
            "Volkswagen",
            "Polo",
            -10_000,
            REGISTRATION_DATE,
        )


def test_maintenance_rule_with_negative_kms_raise_error():
    with pytest.raises(ValueError, match="Kms cannot be lower or equal to zero"):
        MaintenanceRule(kms=-12_000, months=12)


def test_maintenance_rule_with_kms_and_months_equal_to_zero_raise_error():
    with pytest.raises(ValueError, match="At least kms or months must be greater than zero"):
        MaintenanceRule(kms=0, months=0)
