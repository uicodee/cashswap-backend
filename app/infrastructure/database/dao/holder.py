from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.dao.rdb import (
    BaseDAO,
    UserDAO,
    TelegramUserDAO,
    TaskDAO,
    TaskCategoryDAO,
    SubscriptionDAO,
)


class HolderDao:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.base = BaseDAO
        self.user = UserDAO(self.session)
        self.telegram_user = TelegramUserDAO(self.session)
        self.task = TaskDAO(self.session)
        self.task_category = TaskCategoryDAO(self.session)
        self.subscription = SubscriptionDAO(self.session)
