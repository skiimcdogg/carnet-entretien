from fastapi import FastAPI

from carnet_entretien.api.routers import health

app = FastAPI()

app.include_router(health.router)
