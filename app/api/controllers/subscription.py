from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.params import Path
from pydantic import PositiveInt

from app import dto
from app.api import schems
from app.api.dependencies import dao_provider, get_user
from app.infrastructure.database import HolderDao

router = APIRouter(prefix="/subscription")


@router.post(
    path="/", response_model=dto.Subscription, description="Create a subscription", dependencies=[Depends(get_user)]
)
async def create_subscription(
    subscription: schems.Subscription, dao: HolderDao = Depends(dao_provider)
) -> dto.Subscription:
    return await dao.subscription.create(subscription=subscription)


@router.get(
    path="/", response_model=list[dto.Subscription], description="Get subscriptions"
)
async def get_subscriptions(
    dao: HolderDao = Depends(dao_provider),
) -> list[dto.Subscription]:
    return await dao.subscription.get_all()


@router.get(
    path="/{subscription_id}",
    response_model=dto.Subscription,
    description="Get single subscription",
)
async def get_subscription(
    dao: HolderDao = Depends(dao_provider), subscription_id: PositiveInt = Path()
) -> dto.Subscription:
    subscription = await dao.subscription.get_one(subscription_id=subscription_id)
    if subscription is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found"
        )
    return await dao.subscription.get_one(subscription_id=subscription_id)


@router.put(
    path="/{subscription_id}",
    response_model=dto.Subscription,
    description="Update subscription", dependencies=[Depends(get_user)]
)
async def update_subscription(
    subscription: schems.Subscription,
    dao: HolderDao = Depends(dao_provider),
    subscription_id: PositiveInt = Path(),
) -> dto.Subscription:
    current_subscription = await dao.subscription.get_one(
        subscription_id=subscription_id
    )
    if current_subscription is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found"
        )
    return await dao.subscription.update_one(
        subscription_id=subscription_id, subscription=subscription
    )


@router.delete(
    path="/{subscription_id}",
    description="Delete subscription", dependencies=[Depends(get_user)]
)
async def delete_subscription(
    dao: HolderDao = Depends(dao_provider), subscription_id: PositiveInt = Path()
):
    subscription = await dao.subscription.get_one(subscription_id=subscription_id)
    if subscription is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found"
        )
    await dao.subscription.delete_one(subscription_id=subscription_id)
