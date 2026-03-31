import uuid

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.spec_change.models import SpecChangeRequest


async def create_company(client: AsyncClient, name: str = "테스트회사") -> str:
    return (await client.post("/api/companies", json={"name": name})).json()["id"]


async def create_product(client: AsyncClient, company_id: str, name: str = "제품A") -> str:
    return (await client.post("/api/products", json={"company_id": company_id, "name": name})).json()["id"]


async def create_spec_field(client: AsyncClient, name: str = "OCR 정확도") -> str:
    return (
        await client.post(
            "/api/spec-fields",
            json={"category": "tech_spec", "field_name": name, "field_type": "text", "sort_order": 1},
        )
    ).json()["id"]


async def create_change_request(
    db: AsyncSession, product_id: str, spec_field_id: str, old_val: str = "90%", new_val: str = "95%"
) -> str:
    req = SpecChangeRequest(
        product_id=uuid.UUID(product_id),
        spec_field_id=uuid.UUID(spec_field_id),
        old_value=old_val,
        new_value=new_val,
        source_url="https://example.com/article",
        status="pending",
    )
    db.add(req)
    await db.flush()
    return str(req.id)


class TestSpecChangeList:
    async def test_list_empty(self, client: AsyncClient):
        response = await client.get("/api/spec-changes")
        assert response.status_code == 200
        assert response.json()["total"] == 0

    async def test_list_with_filter(self, client: AsyncClient, db: AsyncSession):
        cid = await create_company(client)
        pid = await create_product(client, cid)
        fid = await create_spec_field(client)
        await create_change_request(db, pid, fid)
        await db.commit()

        response = await client.get("/api/spec-changes?status=pending")
        assert response.json()["total"] == 1


class TestSpecChangeApprove:
    async def test_approve(self, client: AsyncClient, db: AsyncSession):
        cid = await create_company(client)
        pid = await create_product(client, cid)
        fid = await create_spec_field(client)

        # set initial spec value
        await client.put(f"/api/products/{pid}/specs", json={"specs": [{"spec_field_id": fid, "value": "90%"}]})

        req_id = await create_change_request(db, pid, fid, "90%", "95%")
        await db.commit()

        response = await client.put(f"/api/spec-changes/{req_id}/approve")
        assert response.status_code == 200
        assert response.json()["status"] == "approved"
        assert response.json()["reviewed_at"] is not None

        # verify spec value was updated
        product = await client.get(f"/api/products/{pid}")
        spec_val = next(sv for sv in product.json()["spec_values"] if sv["spec_field_id"] == fid)
        assert spec_val["value"] == "95%"

    async def test_approve_already_approved(self, client: AsyncClient, db: AsyncSession):
        cid = await create_company(client)
        pid = await create_product(client, cid)
        fid = await create_spec_field(client)
        req_id = await create_change_request(db, pid, fid)
        await db.commit()

        await client.put(f"/api/spec-changes/{req_id}/approve")
        response = await client.put(f"/api/spec-changes/{req_id}/approve")
        assert response.status_code == 400


class TestSpecChangeReject:
    async def test_reject(self, client: AsyncClient, db: AsyncSession):
        cid = await create_company(client)
        pid = await create_product(client, cid)
        fid = await create_spec_field(client)
        req_id = await create_change_request(db, pid, fid)
        await db.commit()

        response = await client.put(
            f"/api/spec-changes/{req_id}/reject",
            json={"reason": "원문에서 확인 불가"},
        )
        assert response.status_code == 200
        assert response.json()["status"] == "rejected"
        assert response.json()["reject_reason"] == "원문에서 확인 불가"

    async def test_reject_not_found(self, client: AsyncClient):
        response = await client.put(
            "/api/spec-changes/00000000-0000-0000-0000-000000000000/reject",
            json={"reason": "test"},
        )
        assert response.status_code == 404
