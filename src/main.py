from fastapi import FastAPI
from src.routers.organization import router as organization_router
from src.routers.storage import router as storage_router


app = FastAPI(
    title="AtomEco API",
    description="API for the AtomEco waste accounting system",
    docs_url="/"
)

app.include_router(organization_router, tags=["Organizations"])
app.include_router(storage_router, tags=["Storages"])
