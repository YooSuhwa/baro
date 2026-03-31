from fastapi import APIRouter, Depends

from app.domains.dashboard.dependencies import get_dashboard_service
from app.domains.dashboard.schemas import DashboardSummaryResponse
from app.domains.dashboard.service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=DashboardSummaryResponse)
async def get_dashboard_summary(service: DashboardService = Depends(get_dashboard_service)):
    return await service.get_summary()
