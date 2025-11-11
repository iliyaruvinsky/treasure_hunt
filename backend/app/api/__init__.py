from fastapi import APIRouter
from . import ingestion, analysis

router = APIRouter()

# Include routers
router.include_router(ingestion.router)
router.include_router(analysis.router)

