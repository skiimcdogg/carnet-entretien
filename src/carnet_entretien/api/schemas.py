from datetime import date

from pydantic import BaseModel, Field


class VehicleCreate(BaseModel):
    brand: str = Field(min_length=1)
    model: str = Field(min_length=1)
    mileage_kms: int = Field(ge=0)
    first_registration_date: date
