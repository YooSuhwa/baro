import uuid

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.news.models import NewsArticle
from app.domains.spec_change.models import SpecChangeRequest


async def create_company(client: AsyncClient, name: str) -> str:
    return (await client.post("/api/companies", json={"name": name})).json()["id"]


class TestDashboardSummary:
    async def test_empty(self, client: AsyncClient):
        response = await client.get("/api/dashboard/summary")
        assert response.status_code == 200
        data = response.json()
        assert data["companies"] == []
        assert data["recent_news"] == []
        assert data["pending_spec_changes_count"] == 0

    async def test_with_data(self, client: AsyncClient, db: AsyncSession):
        cid = await create_company(client, "A사")
        pid = (await client.post("/api/products", json={"company_id": cid, "name": "제품1"})).json()["id"]
        fid = (
            await client.post(
                "/api/spec-fields",
                json={"category": "tech_spec", "field_name": "OCR", "field_type": "text", "sort_order": 1},
            )
        ).json()["id"]

        # add news
        db.add(
            NewsArticle(
                company_id=uuid.UUID(cid),
                title="A사 뉴스",
                url="https://ex.com/1",
                source="naver",
                sentiment="positive",
            )
        )
        # add pending spec change
        db.add(
            SpecChangeRequest(
                product_id=uuid.UUID(pid),
                spec_field_id=uuid.UUID(fid),
                new_value="95%",
                source_url="https://ex.com/src",
                status="pending",
            )
        )
        await db.commit()

        response = await client.get("/api/dashboard/summary")
        data = response.json()
        assert len(data["companies"]) == 1
        assert data["companies"][0]["name"] == "A사"
        assert data["companies"][0]["news_count"] == 1
        assert len(data["recent_news"]) == 1
        assert data["pending_spec_changes_count"] == 1
