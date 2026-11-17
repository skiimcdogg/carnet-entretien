from datetime import date
from uuid import UUID

from pydantic import BaseModel, Field

from carnet_entretien.enums import MaintenanceType


class MaintenanceSchema(BaseModel):
    maintenance_type: MaintenanceType
    maintenance_date: date
    mileage_kms: int = Field(ge=0)


class VehicleCreate(BaseModel):
    brand: str = Field(min_length=1)
    model: str = Field(min_length=1)
    mileage_kms: int = Field(ge=0)
    first_registration_date: date


class VehicleResponse(VehicleCreate):
    id: UUID
    maintenance_history: list[MaintenanceSchema]
