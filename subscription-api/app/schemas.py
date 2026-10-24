from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class SubscriptionStatus(str, Enum):
    ACTIVE = "active"
    CANCELED = "canceled"
    EXPIRED = "expired"


class BillingCycle(str, Enum):
    MONTHLY = "monthly"
    YEARLY = "yearly"


class SubscriptionPlan(BaseModel):
    id: str
    name: str
    description: str
    price_monthly: float = Field(..., ge=0)
    price_yearly: float = Field(..., ge=0)
    features: list[str] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class SubscriptionCreate(BaseModel):
    user_email: EmailStr
    plan_id: str
    billing_cycle: BillingCycle = BillingCycle.MONTHLY


class SubscriptionUpdate(BaseModel):
    plan_id: Optional[str] = None
    billing_cycle: Optional[BillingCycle] = None
    auto_renew: Optional[bool] = None


class SubscriptionResponse(BaseModel):
    id: UUID
    user_email: EmailStr
    plan: SubscriptionPlan
    billing_cycle: BillingCycle
    status: SubscriptionStatus
    start_date: datetime
    end_date: datetime
    auto_renew: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ErrorDetail(BaseModel):
    detail: str
    code: Optional[str] = None
