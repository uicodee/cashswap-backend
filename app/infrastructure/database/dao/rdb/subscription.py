from pydantic import TypeAdapter
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app import dto
from app.api import schems
from app.infrastructure.database.dao.rdb import BaseDAO
from app.infrastructure.database.models import Subscription


class SubscriptionDAO(BaseDAO[Subscription]):
    def __init__(self, session: AsyncSession):
        super().__init__(Subscription, session)

    async def create(self, subscription: schems.Subscription) -> dto.Subscription:
        subscription = Subscription(**subscription.dict())
        self.session.add(subscription)
        await self.session.commit()
        result = await self.session.execute(
            select(Subscription).where(Subscription.id == subscription.id)
        )
        return dto.Subscription.model_validate(result.scalar())

    async def get_all(self) -> list[dto.Subscription]:
        result = await self.session.execute(select(Subscription))
        adapter = TypeAdapter(list[dto.Subscription])
        return adapter.validate_python(result.scalars().all())

    async def get_one(self, subscription_id: int) -> dto.Subscription:
        result = await self.session.execute(
            select(Subscription).where(Subscription.id == subscription_id)
        )
        subscription = result.scalar()
        if subscription is not None:
            return dto.Subscription.model_validate(subscription)

    async def update_one(
        self, subscription_id: int, subscription: schems.Subscription
    ) -> dto.Subscription:
        result = await self.session.execute(
            update(Subscription)
            .where(Subscription.id == subscription_id)
            .values(**subscription.dict())
            .returning(Subscription)
        )
        await self.session.commit()
        return dto.Subscription.model_validate(result.scalar())

    async def delete_one(self, subscription_id: int):
        await self.session.execute(
            delete(Subscription).where(Subscription.id == subscription_id)
        )
        await self.session.commit()
