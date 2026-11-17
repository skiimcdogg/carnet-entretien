from fastapi import FastAPI

from carnet_entretien.api.routers import health, vehicles

app = FastAPI()

app.include_router(health.router)
app.include_router(vehicles.router)
