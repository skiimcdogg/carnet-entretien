from carnet_entretien.models import Maintenance
from datetime import date

maintenance = Maintenance("Vidange", date(2026, 10, 1), 48_000)

print(maintenance)

