from typing import Annotated
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException

from carnet_entretien.api.dependencies import get_vehicle_repository
from carnet_entretien.api.schemas import MaintenanceSchema, VehicleCreate, VehicleResponse
from carnet_entretien.models import Vehicle
from carnet_entretien.repositories.vehicle_repository import VehicleRepository

RepositoryDep = Annotated[VehicleRepository, Depends(get_vehicle_repository)]


def to_response(vehicle_id: UUID, vehicle: Vehicle) -> VehicleResponse:
    return VehicleResponse(
        id=vehicle_id,
        brand=vehicle.brand,
        model=vehicle.model,
        mileage_kms=vehicle.mileage_kms,
        first_registration_date=vehicle.first_registration_date,
        maintenance_history=[
            MaintenanceSchema(
                maintenance_type=m.maintenance_type, maintenance_date=m.maintenance_date, mileage_kms=m.mileage_kms
            )
            for m in vehicle.maintenance_history
        ],
    )


router = APIRouter(prefix="/vehicles", tags=["vehicles"])


@router.post("", status_code=201)
async def create_vehicle(data: VehicleCreate, repository: RepositoryDep) -> VehicleResponse:
    vehicle = Vehicle(**data.model_dump())
    vehicle_id = uuid4()
    repository.save(vehicle_id, vehicle)
    return to_response(vehicle_id, vehicle)


@router.get("/{vehicle_id}")
async def get_vehicle(vehicle_id: UUID, repository: RepositoryDep) -> VehicleResponse:
    vehicle = repository.get(vehicle_id)
    if vehicle is None:
        raise HTTPException(status_code=404, detail="vehicle not found")
    return to_response(vehicle_id, vehicle)


@router.get("")
async def get_all_vehicles(repository: RepositoryDep) -> list[VehicleResponse]:
    vehicles_list = []
    for vehicle_id, vehicle in repository.list_all():
        vehicles_list.append(to_response(vehicle_id, vehicle))

    return vehicles_list


# @router.post("/{vehicle_id}/maintenance")
# async def add_maintenance_to_vehicle(data: MaintenanceSchema, vehicle_id: UUID) -> VehicleResponse:
#     vehicle = vehicles.get(vehicle_id)
#     return
