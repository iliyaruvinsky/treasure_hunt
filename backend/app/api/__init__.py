from fastapi import APIRouter
from . import ingestion, analysis, maintenance, dashboard

router = APIRouter()

# Include routers
router.include_router(ingestion.router)
router.include_router(analysis.router)
router.include_router(maintenance.router)
router.include_router(dashboard.router)

