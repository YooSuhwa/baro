from httpx import AsyncClient


async def setup_compare_data(client: AsyncClient) -> tuple[str, str, str, str]:
    """Setup 2 companies, 2 products, 1 spec field with values. Returns (pid1, pid2, fid, cid)."""
    c1 = (await client.post("/api/companies", json={"name": "한글과컴퓨터"})).json()["id"]
    c2 = (await client.post("/api/companies", json={"name": "사이냅소프트"})).json()["id"]

    p1 = (await client.post("/api/products", json={"company_id": c1, "name": "데이터로더"})).json()["id"]
    p2 = (await client.post("/api/products", json={"company_id": c2, "name": "사이냅 도큐"})).json()["id"]

    fid = (
        await client.post(
            "/api/spec-fields",
            json={"category": "tech_spec", "field_name": "OCR 정확도", "field_type": "text", "sort_order": 1},
        )
    ).json()["id"]

    await client.put(f"/api/products/{p1}/specs", json={"specs": [{"spec_field_id": fid, "value": "97.5%"}]})
    await client.put(f"/api/products/{p2}/specs", json={"specs": [{"spec_field_id": fid, "value": "96.8%"}]})

    return p1, p2, fid, c1


class TestProductCompare:
    async def test_compare_two_products(self, client: AsyncClient):
        p1, p2, fid, _ = await setup_compare_data(client)
        response = await client.get(f"/api/products/compare?ids={p1},{p2}")
        assert response.status_code == 200
        data = response.json()
        assert len(data["products"]) == 2
        assert len(data["categories"]) >= 1

        # find tech_spec category
        tech = next(c for c in data["categories"] if c["name"] == "tech_spec")
        ocr_field = next(f for f in tech["fields"] if f["field_name"] == "OCR 정확도")
        assert ocr_field["values"][p1] == "97.5%"
        assert ocr_field["values"][p2] == "96.8%"

    async def test_compare_one_product_error(self, client: AsyncClient):
        p1, _, _, _ = await setup_compare_data(client)
        response = await client.get(f"/api/products/compare?ids={p1}")
        assert response.status_code == 400

    async def test_compare_too_many_products(self, client: AsyncClient):
        cid = (await client.post("/api/companies", json={"name": "테스트"})).json()["id"]
        pids = []
        for i in range(7):
            p = (await client.post("/api/products", json={"company_id": cid, "name": f"P{i}"})).json()["id"]
            pids.append(p)
        response = await client.get(f"/api/products/compare?ids={','.join(pids)}")
        assert response.status_code == 400

    async def test_compare_missing_value_is_null(self, client: AsyncClient):
        c1 = (await client.post("/api/companies", json={"name": "회사A"})).json()["id"]
        p1 = (await client.post("/api/products", json={"company_id": c1, "name": "제품1"})).json()["id"]
        p2 = (await client.post("/api/products", json={"company_id": c1, "name": "제품2"})).json()["id"]

        fid = (
            await client.post(
                "/api/spec-fields",
                json={"category": "tech_spec", "field_name": "지원포맷", "field_type": "text", "sort_order": 1},
            )
        ).json()["id"]

        # only p1 has a value
        await client.put(f"/api/products/{p1}/specs", json={"specs": [{"spec_field_id": fid, "value": "PDF, HWP"}]})

        response = await client.get(f"/api/products/compare?ids={p1},{p2}")
        data = response.json()
        tech = next(c for c in data["categories"] if c["name"] == "tech_spec")
        field = next(f for f in tech["fields"] if f["field_name"] == "지원포맷")
        assert field["values"][p1] == "PDF, HWP"
        assert field["values"][p2] is None
