from contextlib import asynccontextmanager

from fastapi import FastAPI

from carnet_entretien.api.routers import health, vehicles
from carnet_entretien.db.database import engine
from carnet_entretien.db.tables import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(health.router)
app.include_router(vehicles.router)
