from httpx import AsyncClient


async def create_company(client: AsyncClient, name: str = "테스트회사") -> str:
    resp = await client.post("/api/companies", json={"name": name})
    return resp.json()["id"]


async def create_spec_field(client: AsyncClient, name: str = "OCR 정확도") -> str:
    resp = await client.post(
        "/api/spec-fields",
        json={"category": "tech_spec", "field_name": name, "field_type": "text", "sort_order": 1},
    )
    return resp.json()["id"]


class TestProductCreate:
    async def test_create(self, client: AsyncClient):
        cid = await create_company(client)
        response = await client.post(
            "/api/products",
            json={"company_id": cid, "name": "사이냅 도큐애널라이저", "concept": "문서 구조 분석"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "사이냅 도큐애널라이저"
        assert data["company_id"] == cid

    async def test_create_company_not_found(self, client: AsyncClient):
        response = await client.post(
            "/api/products",
            json={"company_id": "00000000-0000-0000-0000-000000000000", "name": "X"},
        )
        assert response.status_code == 404

    async def test_create_missing_name(self, client: AsyncClient):
        cid = await create_company(client)
        response = await client.post("/api/products", json={"company_id": cid})
        assert response.status_code == 422


class TestProductDetail:
    async def test_get(self, client: AsyncClient):
        cid = await create_company(client)
        create = await client.post("/api/products", json={"company_id": cid, "name": "제품A"})
        pid = create.json()["id"]
        response = await client.get(f"/api/products/{pid}")
        assert response.status_code == 200
        assert response.json()["name"] == "제품A"

    async def test_not_found(self, client: AsyncClient):
        response = await client.get("/api/products/00000000-0000-0000-0000-000000000000")
        assert response.status_code == 404


class TestProductUpdate:
    async def test_update(self, client: AsyncClient):
        cid = await create_company(client)
        create = await client.post("/api/products", json={"company_id": cid, "name": "원래"})
        pid = create.json()["id"]
        response = await client.put(f"/api/products/{pid}", json={"name": "변경"})
        assert response.status_code == 200
        assert response.json()["name"] == "변경"


class TestProductDelete:
    async def test_delete(self, client: AsyncClient):
        cid = await create_company(client)
        create = await client.post("/api/products", json={"company_id": cid, "name": "삭제"})
        pid = create.json()["id"]
        response = await client.delete(f"/api/products/{pid}")
        assert response.status_code == 204


class TestCompanyProducts:
    async def test_list(self, client: AsyncClient):
        cid = await create_company(client)
        await client.post("/api/products", json={"company_id": cid, "name": "A"})
        await client.post("/api/products", json={"company_id": cid, "name": "B"})
        response = await client.get(f"/api/companies/{cid}/products")
        assert response.status_code == 200
        assert len(response.json()) == 2


class TestProductSpecs:
    async def test_bulk_update_specs(self, client: AsyncClient):
        cid = await create_company(client)
        create = await client.post("/api/products", json={"company_id": cid, "name": "제품A"})
        pid = create.json()["id"]
        fid = await create_spec_field(client, "OCR 정확도")

        response = await client.put(
            f"/api/products/{pid}/specs",
            json={"specs": [{"spec_field_id": fid, "value": "97.5%"}]},
        )
        assert response.status_code == 200

        # verify via product detail
        detail = await client.get(f"/api/products/{pid}")
        assert len(detail.json()["spec_values"]) == 1
        assert detail.json()["spec_values"][0]["value"] == "97.5%"

    async def test_bulk_update_upsert(self, client: AsyncClient):
        cid = await create_company(client)
        create = await client.post("/api/products", json={"company_id": cid, "name": "제품A"})
        pid = create.json()["id"]
        fid = await create_spec_field(client, "정확도")

        # first set
        await client.put(f"/api/products/{pid}/specs", json={"specs": [{"spec_field_id": fid, "value": "90%"}]})
        # upsert
        await client.put(f"/api/products/{pid}/specs", json={"specs": [{"spec_field_id": fid, "value": "95%"}]})

        detail = await client.get(f"/api/products/{pid}")
        assert detail.json()["spec_values"][0]["value"] == "95%"
