from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from app.schemas import SubscriptionPlan, SubscriptionResponse


DEFAULT_PLANS: list[SubscriptionPlan] = [
    SubscriptionPlan(
        id="free",
        name="Free Tier",
        description="Basic access for individuals",
        price_monthly=0.0,
        price_yearly=0.0,
        features=["1 Project", "Community Support", "Basic Analytics"],
    ),
    SubscriptionPlan(
        id="pro",
        name="Pro Tier",
        description="Advanced tools for professionals",
        price_monthly=19.99,
        price_yearly=199.99,
        features=["Unlimited Projects", "Priority Support", "Advanced Analytics", "API Access"],
    ),
    SubscriptionPlan(
        id="enterprise",
        name="Enterprise Tier",
        description="Full scale solution for organizations",
        price_monthly=99.99,
        price_yearly=999.99,
        features=["Unlimited Everything", "Dedicated Account Manager", "SLA 99.9%", "Custom Integrations"],
    ),
]


class BaseRepository(ABC):
    @abstractmethod
    async def get_plan(self, plan_id: str) -> Optional[SubscriptionPlan]:
        pass

    @abstractmethod
    async def list_plans(self) -> list[SubscriptionPlan]:
        pass

    @abstractmethod
    async def create_subscription(self, subscription: SubscriptionResponse) -> SubscriptionResponse:
        pass

    @abstractmethod
    async def get_subscription(self, subscription_id: UUID) -> Optional[SubscriptionResponse]:
        pass

    @abstractmethod
    async def get_active_subscription_by_email(self, email: str) -> Optional[SubscriptionResponse]:
        pass

    @abstractmethod
    async def update_subscription(self, subscription: SubscriptionResponse) -> SubscriptionResponse:
        pass

    @abstractmethod
    async def list_subscriptions(self) -> list[SubscriptionResponse]:
        pass


class InMemoryRepository(BaseRepository):
    def __init__(self) -> None:
        self._plans: dict[str, SubscriptionPlan] = {p.id: p for p in DEFAULT_PLANS}
        self._subscriptions: dict[UUID, SubscriptionResponse] = {}

    async def get_plan(self, plan_id: str) -> Optional[SubscriptionPlan]:
        return self._plans.get(plan_id)

    async def list_plans(self) -> list[SubscriptionPlan]:
        return list(self._plans.values())

    async def create_subscription(self, subscription: SubscriptionResponse) -> SubscriptionResponse:
        self._subscriptions[subscription.id] = subscription
        return subscription

    async def get_subscription(self, subscription_id: UUID) -> Optional[SubscriptionResponse]:
        return self._subscriptions.get(subscription_id)

    async def get_active_subscription_by_email(self, email: str) -> Optional[SubscriptionResponse]:
        for sub in self._subscriptions.values():
            if sub.user_email == email and sub.status.value == "active":
                return sub
        return None

    async def update_subscription(self, subscription: SubscriptionResponse) -> SubscriptionResponse:
        self._subscriptions[subscription.id] = subscription
        return subscription

    async def list_subscriptions(self) -> list[SubscriptionResponse]:
        return list(self._subscriptions.values())
