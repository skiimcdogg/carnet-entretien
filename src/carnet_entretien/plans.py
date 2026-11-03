from carnet_entretien.models import MaintenanceRule
from carnet_entretien.enums import MaintenanceType


DEFAULT_MAINTENANCE_PLAN: dict[MaintenanceType, MaintenanceRule] = {
    MaintenanceType.ANNUAL_SERVICE: MaintenanceRule(kms=15_000, months=12),
    MaintenanceType.TIMING_BELT: MaintenanceRule(kms=100_000, months=60),
    MaintenanceType.TRANSMISSION: MaintenanceRule(kms=60_000, months=60),
    MaintenanceType.BRAKE_PADS: MaintenanceRule(kms=40_000),
    MaintenanceType.AC_RECHARGE: MaintenanceRule(months=24),
    MaintenanceType.TIRES: MaintenanceRule(kms=40_000, months=60),
}
