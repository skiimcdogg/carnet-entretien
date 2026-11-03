from enum import StrEnum


class MaintenanceType(StrEnum):
    ANNUAL_SERVICE = "annual_service"
    TIMING_BELT = "timing_belt"
    TRANSMISSION = "Transmission"
    BRAKE_PADS = "brake_pads"
    AC_RECHARGE = "ac_recharge"
    TIRES = "tires"
