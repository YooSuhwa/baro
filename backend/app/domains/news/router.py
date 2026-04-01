import logging
import uuid

from fastapi import APIRouter, BackgroundTasks, Depends, Query

from app.core.schemas import PaginatedResponse
from app.domains.news.dependencies import get_news_service
from app.domains.news.schemas import CollectRequest, CollectResponse, NewsCompareResponse, NewsResponse
from app.domains.news.service import NewsService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/news", tags=["news"])


@router.get("", response_model=PaginatedResponse[NewsResponse])
async def list_news(
    company_id: uuid.UUID | None = Query(None),
    sentiment: str | None = Query(None),
    period: str | None = Query(None),
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    service: NewsService = Depends(get_news_service),
):
    return await service.list_filtered(company_id, sentiment, period, offset, limit)


@router.get("/compare", response_model=NewsCompareResponse)
async def compare_news(
    company_ids: str = Query(..., description="Comma-separated company IDs"),
    period: str = Query("1w"),
    service: NewsService = Depends(get_news_service),
):
    ids = [uuid.UUID(cid.strip()) for cid in company_ids.split(",") if cid.strip()]
    return await service.compare(ids, period)


async def _run_pipeline_background(company_id: uuid.UUID | None) -> None:
    """Run the news pipeline with its own DB session (not request-scoped)."""
    from app.core.database import async_session
    from app.services.news_pipeline import run_collection_pipeline

    async with async_session() as session:
        try:
            result = await run_collection_pipeline(session, company_id)
            logger.info(f"Background collection complete: {result}")
        except Exception as e:
            logger.error(f"Background collection failed: {e}")


@router.post("/collect", response_model=CollectResponse)
async def trigger_collect(
    data: CollectRequest,
    background_tasks: BackgroundTasks,
):
    background_tasks.add_task(_run_pipeline_background, data.company_id)
    return CollectResponse(message="뉴스 수집이 시작되었습니다.", company_id=data.company_id)
