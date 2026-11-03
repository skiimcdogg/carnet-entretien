from datetime import date

from carnet_entretien.enums import MaintenanceType
from carnet_entretien.models import Maintenance, Vehicle, MaintenancePlan

my_sandero = Vehicle("Dacia", "Sandero", 80_000)

maintenance_1 = Maintenance(MaintenanceType.ANNUAL_SERVICE, date(2026, 10, 1), 48_000)
maintenance_2 = Maintenance(MaintenanceType.ANNUAL_SERVICE, date(2026, 10, 1), 60_000)

my_sandero.add_maintenance(maintenance_1, date.today())
my_sandero.add_maintenance(maintenance_2, date.today())

print(my_sandero.maintenance_history)

print(my_sandero.find_last_maintenance(MaintenanceType.ANNUAL_SERVICE))

test = MaintenancePlan(None, 15)

print(test)
