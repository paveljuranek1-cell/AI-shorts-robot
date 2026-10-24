from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, status
from app.auth import verify_api_key
from app.repository import BaseRepository, InMemoryRepository
from app.schemas import (
    SubscriptionCreate,
    SubscriptionPlan,
    SubscriptionResponse,
    SubscriptionUpdate,
)
from app.service import SubscriptionService

router = APIRouter()

# Global repository instance for app state
_repo_instance = InMemoryRepository()


def get_service() -> SubscriptionService:
    return SubscriptionService(_repo_instance)


@router.get(
    "/plans",
    response_model=list[SubscriptionPlan],
    summary="List available subscription plans",
)
async def list_plans(
    service: Annotated[SubscriptionService, Depends(get_service)]
) -> list[SubscriptionPlan]:
    return await service.list_plans()


@router.get(
    "/plans/{plan_id}",
    response_model=SubscriptionPlan,
    summary="Get details of a specific subscription plan",
)
async def get_plan(
    plan_id: str,
    service: Annotated[SubscriptionService, Depends(get_service)],
) -> SubscriptionPlan:
    return await service.get_plan(plan_id)


@router.post(
    "/subscriptions",
    response_model=SubscriptionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new subscription",
    dependencies=[Depends(verify_api_key)],
)
async def create_subscription(
    payload: SubscriptionCreate,
    service: Annotated[SubscriptionService, Depends(get_service)],
) -> SubscriptionResponse:
    return await service.create_subscription(payload)


@router.get(
    "/subscriptions",
    response_model=list[SubscriptionResponse],
    summary="List all subscriptions",
    dependencies=[Depends(verify_api_key)],
)
async def list_subscriptions(
    service: Annotated[SubscriptionService, Depends(get_service)],
) -> list[SubscriptionResponse]:
    return await service.list_subscriptions()


@router.get(
    "/subscriptions/{subscription_id}",
    response_model=SubscriptionResponse,
    summary="Get subscription by ID",
    dependencies=[Depends(verify_api_key)],
)
async def get_subscription(
    subscription_id: UUID,
    service: Annotated[SubscriptionService, Depends(get_service)],
) -> SubscriptionResponse:
    return await service.get_subscription(subscription_id)


@router.patch(
    "/subscriptions/{subscription_id}",
    response_model=SubscriptionResponse,
    summary="Update subscription plan, cycle, or auto-renew",
    dependencies=[Depends(verify_api_key)],
)
async def update_subscription(
    subscription_id: UUID,
    payload: SubscriptionUpdate,
    service: Annotated[SubscriptionService, Depends(get_service)],
) -> SubscriptionResponse:
    return await service.update_subscription(subscription_id, payload)


@router.delete(
    "/subscriptions/{subscription_id}",
    response_model=SubscriptionResponse,
    summary="Cancel a subscription",
    dependencies=[Depends(verify_api_key)],
)
async def cancel_subscription(
    subscription_id: UUID,
    service: Annotated[SubscriptionService, Depends(get_service)],
) -> SubscriptionResponse:
    return await service.cancel_subscription(subscription_id)
