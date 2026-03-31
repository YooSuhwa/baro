from httpx import AsyncClient


class TestCompanyCreate:
    async def test_create_success(self, client: AsyncClient):
        response = await client.post(
            "/api/companies",
            json={
                "name": "사이냅소프트",
                "founded_at": "2000-07-26",
                "employee_count": 80,
                "revenue": "127억(2023)",
                "website_url": "https://www.synapsoft.co.kr",
                "search_keywords": ["사이냅소프트", "사이냅 OCR"],
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "사이냅소프트"
        assert len(data["search_keywords"]) == 2
        assert "id" in data
        assert data["employee_count"] == 80

    async def test_create_minimal(self, client: AsyncClient):
        response = await client.post("/api/companies", json={"name": "최소등록"})
        assert response.status_code == 201
        assert response.json()["name"] == "최소등록"
        assert response.json()["search_keywords"] == []

    async def test_create_duplicate(self, client: AsyncClient):
        await client.post("/api/companies", json={"name": "사이냅소프트"})
        response = await client.post("/api/companies", json={"name": "사이냅소프트"})
        assert response.status_code == 409
        assert response.json()["error"] == "DUPLICATE_COMPANY"

    async def test_create_missing_name(self, client: AsyncClient):
        response = await client.post("/api/companies", json={})
        assert response.status_code == 422


class TestCompanyList:
    async def test_list_empty(self, client: AsyncClient):
        response = await client.get("/api/companies")
        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 0

    async def test_list_with_data(self, client: AsyncClient):
        await client.post("/api/companies", json={"name": "A사"})
        await client.post("/api/companies", json={"name": "B사"})
        response = await client.get("/api/companies")
        assert response.json()["total"] == 2
        assert len(response.json()["items"]) == 2

    async def test_list_pagination(self, client: AsyncClient):
        for i in range(5):
            await client.post("/api/companies", json={"name": f"회사{i}"})
        response = await client.get("/api/companies?offset=0&limit=2")
        data = response.json()
        assert len(data["items"]) == 2
        assert data["total"] == 5


class TestCompanyDetail:
    async def test_get_company(self, client: AsyncClient):
        create = await client.post("/api/companies", json={"name": "테스트"})
        cid = create.json()["id"]
        response = await client.get(f"/api/companies/{cid}")
        assert response.status_code == 200
        assert response.json()["name"] == "테스트"

    async def test_not_found(self, client: AsyncClient):
        response = await client.get("/api/companies/00000000-0000-0000-0000-000000000000")
        assert response.status_code == 404


class TestCompanyUpdate:
    async def test_update_name(self, client: AsyncClient):
        create = await client.post("/api/companies", json={"name": "원래"})
        cid = create.json()["id"]
        response = await client.put(f"/api/companies/{cid}", json={"name": "새이름"})
        assert response.status_code == 200
        assert response.json()["name"] == "새이름"

    async def test_update_keywords(self, client: AsyncClient):
        create = await client.post("/api/companies", json={"name": "A", "search_keywords": ["old"]})
        cid = create.json()["id"]
        response = await client.put(f"/api/companies/{cid}", json={"search_keywords": ["new1", "new2"]})
        assert response.status_code == 200
        assert len(response.json()["search_keywords"]) == 2

    async def test_update_duplicate_name(self, client: AsyncClient):
        await client.post("/api/companies", json={"name": "A사"})
        create_b = await client.post("/api/companies", json={"name": "B사"})
        cid = create_b.json()["id"]
        response = await client.put(f"/api/companies/{cid}", json={"name": "A사"})
        assert response.status_code == 409


class TestCompanyDelete:
    async def test_delete(self, client: AsyncClient):
        create = await client.post("/api/companies", json={"name": "삭제"})
        cid = create.json()["id"]
        response = await client.delete(f"/api/companies/{cid}")
        assert response.status_code == 204
        assert (await client.get(f"/api/companies/{cid}")).status_code == 404

    async def test_delete_not_found(self, client: AsyncClient):
        response = await client.delete("/api/companies/00000000-0000-0000-0000-000000000000")
        assert response.status_code == 404
