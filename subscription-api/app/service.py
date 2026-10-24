from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID, uuid4
from fastapi import HTTPException, status
from app.repository import BaseRepository
from app.schemas import (
    BillingCycle,
    SubscriptionCreate,
    SubscriptionPlan,
    SubscriptionResponse,
    SubscriptionStatus,
    SubscriptionUpdate,
)


class SubscriptionService:
    def __init__(self, repo: BaseRepository) -> None:
        self.repo = repo

    async def list_plans(self) -> list[SubscriptionPlan]:
        return await self.repo.list_plans()

    async def get_plan(self, plan_id: str) -> SubscriptionPlan:
        plan = await self.repo.get_plan(plan_id)
        if not plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Plan '{plan_id}' not found.",
            )
        return plan

    async def create_subscription(self, payload: SubscriptionCreate) -> SubscriptionResponse:
        # Check if plan exists
        plan = await self.get_plan(payload.plan_id)

        # Check if user already has an active subscription
        existing = await self.repo.get_active_subscription_by_email(payload.user_email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User '{payload.user_email}' already has an active subscription.",
            )

        now = datetime.now(timezone.utc)
        duration = timedelta(days=365) if payload.billing_cycle == BillingCycle.YEARLY else timedelta(days=30)
        end_date = now + duration

        sub = SubscriptionResponse(
            id=uuid4(),
            user_email=payload.user_email,
            plan=plan,
            billing_cycle=payload.billing_cycle,
            status=SubscriptionStatus.ACTIVE,
            start_date=now,
            end_date=end_date,
            auto_renew=True,
            created_at=now,
            updated_at=now,
        )

        return await self.repo.create_subscription(sub)

    async def get_subscription(self, subscription_id: UUID) -> SubscriptionResponse:
        sub = await self.repo.get_subscription(subscription_id)
        if not sub:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Subscription '{subscription_id}' not found.",
            )
        return sub

    async def list_subscriptions(self) -> list[SubscriptionResponse]:
        return await self.repo.list_subscriptions()

    async def update_subscription(
        self, subscription_id: UUID, payload: SubscriptionUpdate
    ) -> SubscriptionResponse:
        sub = await self.get_subscription(subscription_id)

        if sub.status == SubscriptionStatus.CANCELED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot update a canceled subscription.",
            )

        now = datetime.now(timezone.utc)
        updated_fields = {}

        if payload.plan_id is not None and payload.plan_id != sub.plan.id:
            new_plan = await self.get_plan(payload.plan_id)
            updated_fields["plan"] = new_plan

        if payload.billing_cycle is not None and payload.billing_cycle != sub.billing_cycle:
            updated_fields["billing_cycle"] = payload.billing_cycle
            # Recalculate end date from current start or now
            duration = timedelta(days=365) if payload.billing_cycle == BillingCycle.YEARLY else timedelta(days=30)
            updated_fields["end_date"] = sub.start_date + duration

        if payload.auto_renew is not None:
            updated_fields["auto_renew"] = payload.auto_renew

        updated_fields["updated_at"] = now

        updated_sub = sub.model_copy(update=updated_fields)
        return await self.repo.update_subscription(updated_sub)

    async def cancel_subscription(self, subscription_id: UUID) -> SubscriptionResponse:
        sub = await self.get_subscription(subscription_id)

        if sub.status == SubscriptionStatus.CANCELED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Subscription is already canceled.",
            )

        now = datetime.now(timezone.utc)
        updated_sub = sub.model_copy(
            update={
                "status": SubscriptionStatus.CANCELED,
                "auto_renew": False,
                "updated_at": now,
            }
        )
        return await self.repo.update_subscription(updated_sub)
