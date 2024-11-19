from datetime import datetime

from pydantic import TypeAdapter
from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import rank

from app import dto
from app.api import schems
from app.infrastructure.database.dao.rdb import BaseDAO
from app.infrastructure.database.models import TelegramUser


class TelegramUserDAO(BaseDAO[TelegramUser]):
    def __init__(self, session: AsyncSession):
        super().__init__(TelegramUser, session)

    async def create(
        self,
        telegram_id: int,
        username: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
        referrer_id: int | None = None,
    ) -> dto.TelegramUser:
        telegram_user = TelegramUser(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            referrer_id=referrer_id,
        )
        self.session.add(telegram_user)
        await self.session.commit()
        return dto.TelegramUser.from_orm(telegram_user)

    async def get_all_referrals(self, telegram_id: int) -> list[dto.TelegramUser]:
        result = await self.session.execute(
            select(TelegramUser).where(TelegramUser.referrer_id == telegram_id)
        )
        adapter = TypeAdapter(list[dto.TelegramUser])
        return adapter.validate_python(result.scalars().all())

    async def get_all(self) -> list[dto.TelegramUser]:
        result = await self.session.execute(select(TelegramUser))
        adapter = TypeAdapter(list[dto.TelegramUser])
        return adapter.validate_python(result.scalars().all())

    async def get_telegram_user(self, telegram_id: int) -> dto.TelegramUser:
        result = await self.session.execute(
            select(TelegramUser).filter(TelegramUser.telegram_id == telegram_id)
        )
        telegram_user = result.scalar()
        if telegram_user is not None:
            return dto.TelegramUser.from_orm(telegram_user)

    async def get_user_rank(self, telegram_id: int):
        subquery = select(
            TelegramUser.telegram_id,
            TelegramUser.balance,
            func.row_number()
            .over(order_by=[TelegramUser.balance.desc(), TelegramUser.created_at.asc()])
            .label("user_rank"),
        ).subquery()

        stmt = select(subquery.c.user_rank).where(subquery.c.telegram_id == telegram_id)
        result = await self.session.execute(stmt)
        return result.scalar()

    async def get_users_by_rank(self):
        subquery = (
            select(
                TelegramUser,
                func.row_number()
                .over(
                    order_by=[
                        TelegramUser.balance.desc(),
                        TelegramUser.created_at.asc(),
                    ]
                )
                .label("place"),
            )
            .order_by(TelegramUser.balance.desc(), TelegramUser.created_at.asc())
            .limit(50)
            .subquery()
        )

        result = await self.session.execute(select(subquery))
        adapter = TypeAdapter(list[dto.TelegramUser])
        return adapter.validate_python(result.mappings().all())

    async def update_referrals(
        self, telegram_id: int, tickets: int, referrals: int, balance: float
    ) -> dto.TelegramUser:
        result = await self.session.execute(
            update(TelegramUser)
            .where(TelegramUser.telegram_id == telegram_id)
            .values(referrals=referrals, tickets=tickets, balance=balance)
            .returning(TelegramUser)
        )
        await self.session.commit()
        return dto.TelegramUser.model_validate(result.scalar())

    async def update_user_extra_balance(
        self, telegram_id: int, extra_balance: float
    ) -> dto.TelegramUser:
        result = await self.session.execute(
            update(TelegramUser)
            .where(TelegramUser.telegram_id == telegram_id)
            .values(extra_balance=extra_balance)
            .returning(TelegramUser)
        )
        await self.session.commit()
        return dto.TelegramUser.model_validate(result.scalar())

    async def update_user_tickets(
        self, telegram_id: int, tickets: int
    ) -> dto.TelegramUser:
        result = await self.session.execute(
            update(TelegramUser)
            .where(TelegramUser.telegram_id == telegram_id)
            .values(tickets=tickets)
            .returning(TelegramUser)
        )
        await self.session.commit()
        return dto.TelegramUser.model_validate(result.scalar())

    async def update_user_balance(
        self, telegram_id: int, balance: float
    ) -> dto.TelegramUser:
        result = await self.session.execute(
            update(TelegramUser)
            .where(TelegramUser.telegram_id == telegram_id)
            .values(balance=balance)
            .returning(TelegramUser)
        )
        await self.session.commit()
        return dto.TelegramUser.model_validate(result.scalar())

    async def update_balance(
        self,
        telegram_id: int,
        balance: float,
        last_farm: datetime,
        next_farm: datetime,
    ) -> dto.TelegramUser:
        result = await self.session.execute(
            update(TelegramUser)
            .where(TelegramUser.telegram_id == telegram_id)
            .values(balance=balance, last_farm=last_farm, next_farm=next_farm)
            .returning(TelegramUser)
        )
        await self.session.commit()
        return dto.TelegramUser.model_validate(result.scalar())

    async def update_last_daily_reward(
        self,
        telegram_id: int,
        last_daily_reward: datetime,
    ) -> dto.TelegramUser:
        result = await self.session.execute(
            update(TelegramUser)
            .where(TelegramUser.telegram_id == telegram_id)
            .values(last_daily_reward=last_daily_reward)
            .returning(TelegramUser)
        )
        await self.session.commit()
        return dto.TelegramUser.model_validate(result.scalar())

    async def update_last_action(
        self,
        telegram_id: int,
        last_action: datetime,
    ) -> dto.TelegramUser:
        result = await self.session.execute(
            update(TelegramUser)
            .where(TelegramUser.telegram_id == telegram_id)
            .values(last_action=last_action)
            .returning(TelegramUser)
        )
        await self.session.commit()
        return dto.TelegramUser.model_validate(result.scalar())

    async def update_days_active(
        self, telegram_id: int, days_active: int, last_days_active: int
    ) -> dto.TelegramUser:
        result = await self.session.execute(
            update(TelegramUser)
            .where(TelegramUser.telegram_id == telegram_id)
            .values(days_active=days_active, last_days_active=last_days_active)
            .returning(TelegramUser)
        )
        await self.session.commit()
        return dto.TelegramUser.model_validate(result.scalar())

    async def update_one(
        self, telegram_id: int, telegram_user: schems.UpdateTelegramUser
    ) -> dto.TelegramUser:
        result = await self.session.execute(
            update(TelegramUser)
            .where(TelegramUser.telegram_id == telegram_id)
            .values(**telegram_user.dict())
            .returning(TelegramUser)
        )
        await self.session.commit()
        return dto.TelegramUser.model_validate(result.scalar())
