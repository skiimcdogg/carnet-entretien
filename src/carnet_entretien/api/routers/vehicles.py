from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException

from carnet_entretien.api.schemas import MaintenanceSchema, VehicleCreate, VehicleResponse
from carnet_entretien.api.storage import vehicles
from carnet_entretien.models import Vehicle


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
async def create_vehicle(data: VehicleCreate) -> VehicleResponse:
    vehicle = Vehicle(**data.model_dump())
    vehicle_id = uuid4()
    vehicles[vehicle_id] = vehicle
    return to_response(vehicle_id, vehicle)


@router.get("/{vehicle_id}")
async def get_vehicle(vehicle_id: UUID) -> VehicleResponse:
    vehicle = vehicles.get(vehicle_id)
    if vehicle is None:
        raise HTTPException(status_code=404, detail="vehicle not found")
    return to_response(vehicle_id, vehicle)
