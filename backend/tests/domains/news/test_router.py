import uuid

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.news.models import NewsArticle


async def create_company(client: AsyncClient, name: str = "테스트회사") -> str:
    return (await client.post("/api/companies", json={"name": name})).json()["id"]


async def insert_news(db: AsyncSession, company_id: str, title: str, sentiment: str = "positive") -> None:
    article = NewsArticle(
        company_id=uuid.UUID(company_id),
        title=title,
        url=f"https://example.com/{uuid.uuid4()}",
        source="naver",
        sentiment=sentiment,
        summary=f"{title} 요약",
    )
    db.add(article)
    await db.flush()


class TestNewsList:
    async def test_list_empty(self, client: AsyncClient):
        response = await client.get("/api/news")
        assert response.status_code == 200
        assert response.json()["total"] == 0

    async def test_list_with_data(self, client: AsyncClient, db: AsyncSession):
        cid = await create_company(client)
        await insert_news(db, cid, "뉴스1")
        await insert_news(db, cid, "뉴스2")
        await db.commit()
        response = await client.get("/api/news")
        assert response.json()["total"] == 2

    async def test_filter_by_company(self, client: AsyncClient, db: AsyncSession):
        c1 = await create_company(client, "A사")
        c2 = await create_company(client, "B사")
        await insert_news(db, c1, "A뉴스")
        await insert_news(db, c2, "B뉴스")
        await db.commit()
        response = await client.get(f"/api/news?company_id={c1}")
        assert response.json()["total"] == 1
        assert response.json()["items"][0]["title"] == "A뉴스"

    async def test_filter_by_sentiment(self, client: AsyncClient, db: AsyncSession):
        cid = await create_company(client)
        await insert_news(db, cid, "긍정", "positive")
        await insert_news(db, cid, "부정", "negative")
        await db.commit()
        response = await client.get("/api/news?sentiment=positive")
        assert response.json()["total"] == 1


class TestNewsCompare:
    async def test_compare(self, client: AsyncClient, db: AsyncSession):
        c1 = await create_company(client, "A사")
        c2 = await create_company(client, "B사")
        await insert_news(db, c1, "A긍정", "positive")
        await insert_news(db, c1, "A부정", "negative")
        await insert_news(db, c2, "B중립", "neutral")
        await db.commit()

        response = await client.get(f"/api/news/compare?company_ids={c1},{c2}&period=1m")
        assert response.status_code == 200
        data = response.json()
        assert len(data["companies"]) == 2
        assert data["companies"][0]["total_count"] == 2
        assert data["companies"][1]["total_count"] == 1


class TestNewsCollect:
    async def test_trigger_collect(self, client: AsyncClient):
        cid = await create_company(client)
        response = await client.post("/api/news/collect", json={"company_id": cid})
        assert response.status_code == 200
        assert "수집이 시작" in response.json()["message"]
