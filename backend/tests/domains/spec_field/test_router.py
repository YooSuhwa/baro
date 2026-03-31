from httpx import AsyncClient


class TestSpecFieldCreate:
    async def test_create(self, client: AsyncClient):
        response = await client.post(
            "/api/spec-fields",
            json={"category": "tech_spec", "field_name": "OCR 정확도", "field_type": "text", "sort_order": 1},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["field_name"] == "OCR 정확도"
        assert data["category"] == "tech_spec"

    async def test_create_template(self, client: AsyncClient):
        response = await client.post(
            "/api/spec-fields",
            json={
                "category": "company_info",
                "field_name": "업력",
                "field_type": "text",
                "is_template": True,
                "sort_order": 0,
            },
        )
        assert response.status_code == 201
        assert response.json()["is_template"] is True


class TestSpecFieldList:
    async def test_list_empty(self, client: AsyncClient):
        response = await client.get("/api/spec-fields")
        assert response.status_code == 200
        assert response.json() == []

    async def test_list_ordered(self, client: AsyncClient):
        await client.post(
            "/api/spec-fields",
            json={"category": "company_info", "field_name": "매출", "field_type": "text", "sort_order": 2},
        )
        await client.post(
            "/api/spec-fields",
            json={"category": "company_info", "field_name": "업력", "field_type": "text", "sort_order": 1},
        )
        response = await client.get("/api/spec-fields")
        items = response.json()
        assert items[0]["field_name"] == "업력"
        assert items[1]["field_name"] == "매출"


class TestSpecFieldUpdate:
    async def test_update(self, client: AsyncClient):
        create = await client.post(
            "/api/spec-fields",
            json={"category": "tech_spec", "field_name": "원래", "field_type": "text", "sort_order": 1},
        )
        fid = create.json()["id"]
        response = await client.put(f"/api/spec-fields/{fid}", json={"field_name": "변경됨"})
        assert response.status_code == 200
        assert response.json()["field_name"] == "변경됨"


class TestSpecFieldDelete:
    async def test_delete(self, client: AsyncClient):
        create = await client.post(
            "/api/spec-fields",
            json={"category": "tech_spec", "field_name": "삭제", "field_type": "text", "sort_order": 1},
        )
        fid = create.json()["id"]
        response = await client.delete(f"/api/spec-fields/{fid}")
        assert response.status_code == 204
