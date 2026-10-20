import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from app.auth import EXPECTED_API_KEY
from app.main import app
from app.repository import InMemoryRepository
from app.router import get_service
from app.service import SubscriptionService


@pytest.fixture
def repo():
    return InMemoryRepository()


@pytest.fixture
def service(repo):
    return SubscriptionService(repo)


@pytest_asyncio.fixture
async def client(repo):
    app.dependency_overrides[get_service] = lambda: SubscriptionService(repo)
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_health_check(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


@pytest.mark.asyncio
async def test_list_plans(client):
    response = await client.get("/api/v1/plans")
    assert response.status_code == 200
    plans = response.json()
    assert len(plans) == 3
    plan_ids = [p["id"] for p in plans]
    assert "free" in plan_ids
    assert "pro" in plan_ids
    assert "enterprise" in plan_ids


@pytest.mark.asyncio
async def test_get_plan(client):
    response = await client.get("/api/v1/plans/pro")
    assert response.status_code == 200
    plan = response.json()
    assert plan["id"] == "pro"
    assert plan["price_monthly"] == 19.99

    response_404 = await client.get("/api/v1/plans/nonexistent")
    assert response_404.status_code == 404


@pytest.mark.asyncio
async def test_create_subscription_auth_required(client):
    # Without header -> 401
    res_no_auth = await client.post(
        "/api/v1/subscriptions",
        json={"user_email": "test@example.com", "plan_id": "pro"},
    )
    assert res_no_auth.status_code == 401

    # Invalid header -> 403
    res_invalid_auth = await client.post(
        "/api/v1/subscriptions",
        json={"user_email": "test@example.com", "plan_id": "pro"},
        headers={"X-API-Key": "wrong-key"},
    )
    assert res_invalid_auth.status_code == 403


@pytest.mark.asyncio
async def test_create_and_get_subscription(client):
    headers = {"X-API-Key": EXPECTED_API_KEY}
    payload = {
        "user_email": "user@example.com",
        "plan_id": "pro",
        "billing_cycle": "monthly",
    }

    res = await client.post("/api/v1/subscriptions", json=payload, headers=headers)
    assert res.status_code == 201
    data = res.json()
    sub_id = data["id"]
    assert data["user_email"] == "user@example.com"
    assert data["plan"]["id"] == "pro"
    assert data["status"] == "active"

    # Get subscription
    get_res = await client.get(f"/api/v1/subscriptions/{sub_id}", headers=headers)
    assert get_res.status_code == 200
    assert get_res.json()["id"] == sub_id


@pytest.mark.asyncio
async def test_create_duplicate_active_subscription_conflict(client):
    headers = {"X-API-Key": EXPECTED_API_KEY}
    payload = {
        "user_email": "user@example.com",
        "plan_id": "pro",
    }

    res1 = await client.post("/api/v1/subscriptions", json=payload, headers=headers)
    assert res1.status_code == 201

    res2 = await client.post("/api/v1/subscriptions", json=payload, headers=headers)
    assert res2.status_code == 409
    assert "already has an active subscription" in res2.json()["detail"]


@pytest.mark.asyncio
async def test_update_subscription(client):
    headers = {"X-API-Key": EXPECTED_API_KEY}
    create_res = await client.post(
        "/api/v1/subscriptions",
        json={"user_email": "user@example.com", "plan_id": "free"},
        headers=headers,
    )
    sub_id = create_res.json()["id"]

    # Upgrade to pro and yearly billing
    update_res = await client.patch(
        f"/api/v1/subscriptions/{sub_id}",
        json={"plan_id": "pro", "billing_cycle": "yearly"},
        headers=headers,
    )
    assert update_res.status_code == 200
    updated_data = update_res.json()
    assert updated_data["plan"]["id"] == "pro"
    assert updated_data["billing_cycle"] == "yearly"


@pytest.mark.asyncio
async def test_cancel_subscription(client):
    headers = {"X-API-Key": EXPECTED_API_KEY}
    create_res = await client.post(
        "/api/v1/subscriptions",
        json={"user_email": "user@example.com", "plan_id": "pro"},
        headers=headers,
    )
    sub_id = create_res.json()["id"]

    # Cancel subscription
    cancel_res = await client.delete(f"/api/v1/subscriptions/{sub_id}", headers=headers)
    assert cancel_res.status_code == 200
    data = cancel_res.json()
    assert data["status"] == "canceled"
    assert data["auto_renew"] is False

    # Try canceling again -> 400
    cancel_again = await client.delete(f"/api/v1/subscriptions/{sub_id}", headers=headers)
    assert cancel_again.status_code == 400

    # Try updating canceled subscription -> 400
    update_canceled = await client.patch(
        f"/api/v1/subscriptions/{sub_id}",
        json={"plan_id": "enterprise"},
        headers=headers,
    )
    assert update_canceled.status_code == 400


@pytest.mark.asyncio
async def test_validation_errors(client):
    headers = {"X-API-Key": EXPECTED_API_KEY}
    # Invalid email
    invalid_email_res = await client.post(
        "/api/v1/subscriptions",
        json={"user_email": "not-an-email", "plan_id": "pro"},
        headers=headers,
    )
    assert invalid_email_res.status_code == 422
