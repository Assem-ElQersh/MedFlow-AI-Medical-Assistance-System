from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth,
    patients,
    diagnosis,
    radiology,
    emergency,
    specialists
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(patients.router, prefix="/patients", tags=["patients"])
api_router.include_router(diagnosis.router, prefix="/diagnosis", tags=["diagnosis"])
api_router.include_router(radiology.router, prefix="/radiology", tags=["radiology"])
api_router.include_router(emergency.router, prefix="/emergency", tags=["emergency"])
api_router.include_router(specialists.router, prefix="/specialists", tags=["specialists"]) 