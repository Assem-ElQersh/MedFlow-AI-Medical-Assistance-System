from fastapi import APIRouter
from app.api.endpoints import pneumonia

api_router = APIRouter()

# Include pneumonia endpoints
api_router.include_router(
    pneumonia.router,
    prefix="/pneumonia",
    tags=["pneumonia"]
) 