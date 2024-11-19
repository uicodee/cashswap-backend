from pydantic import TypeAdapter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import dto
from app.api import schems
from app.infrastructure.database.dao.rdb import BaseDAO
from app.infrastructure.database.models import TaskCategory


class TaskCategoryDAO(BaseDAO[TaskCategory]):
    def __init__(self, session: AsyncSession):
        super().__init__(TaskCategory, session)

    async def create(self, task_category: schems.TaskCategory) -> dto.TaskCategory:
        task_category = TaskCategory(**task_category.dict())
        self.session.add(task_category)
        await self.session.commit()
        return dto.TaskCategory.model_validate(task_category)

    async def get_all(self) -> list[dto.TaskCategory]:
        result = await self.session.execute(select(TaskCategory))
        adapter = TypeAdapter(list[dto.TaskCategory])
        return adapter.validate_python(result.scalars().all())

    async def get_one(self, task_category_id: int) -> dto.TaskCategory:
        result = await self.session.execute(
            select(TaskCategory).where(TaskCategory.id == task_category_id)
        )
        task_category = result.scalar()
        if task_category is not None:
            return dto.TaskCategory.model_validate(task_category)
