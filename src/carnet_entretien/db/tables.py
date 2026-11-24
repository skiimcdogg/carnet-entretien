from datetime import date
from uuid import UUID

from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from carnet_entretien.enums import MaintenanceType


class Base(DeclarativeBase):
    "All classes mother"


class VehicleRow(Base):
    __tablename__ = "vehicles"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    brand: Mapped[str]
    model: Mapped[str]
    mileage_kms: Mapped[int]
    first_registration_date: Mapped[date]

    maintenance_history: Mapped[list[MaintenanceRow]] = relationship(cascade="all, delete-orphan")


class MaintenanceRow(Base):
    __tablename__ = "maintenances"

    id: Mapped[int] = mapped_column(primary_key=True)
    vehicle_id: Mapped[UUID] = mapped_column(ForeignKey("vehicles.id"))
    maintenance_type: Mapped[MaintenanceType] = mapped_column(
        SqlEnum(MaintenanceType, values_callable=lambda enum: [member.value for member in enum])
    )
    maintenance_date: Mapped[date]
    mileage_kms: Mapped[int]
