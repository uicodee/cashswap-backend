from pydantic import TypeAdapter
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app import dto
from app.api import schems
from app.infrastructure.database.dao.rdb import BaseDAO
from app.infrastructure.database.models import Task, CompletedTask


class TaskDAO(BaseDAO[Task]):
    def __init__(self, session: AsyncSession):
        super().__init__(Task, session)

    async def create(self, task: schems.Task) -> dto.Task:
        task = Task(**task.dict())
        self.session.add(task)
        await self.session.commit()
        result = await self.session.execute(select(Task).where(Task.id == task.id))
        return dto.Task.model_validate(result.scalar())

    async def create_completed_task(self, task_id: int, telegram_user_id: int):
        completed_task = CompletedTask(
            task_id=task_id, telegram_user_id=telegram_user_id
        )
        self.session.add(completed_task)
        await self.session.commit()

    async def get_completed_tasks(self, telegram_user_id: int) -> list[int]:
        result = await self.session.execute(
            select(CompletedTask.task_id).where(
                CompletedTask.telegram_user_id == telegram_user_id
            )
        )
        adapter = TypeAdapter(list[int])
        return adapter.validate_python(result.scalars().all())

    async def get_all(self) -> list[dto.Task]:
        result = await self.session.execute(select(Task))
        adapter = TypeAdapter(list[dto.Task])
        return adapter.validate_python(result.scalars().all())

    async def get_one(self, task_id: int) -> dto.Task:
        result = await self.session.execute(select(Task).where(Task.id == task_id))
        task = result.scalar()
        if task is not None:
            return dto.Task.model_validate(task)

    async def update_one(self, task_id: int, task: schems.Task) -> dto.Task:
        result = await self.session.execute(
            update(Task).where(Task.id == task_id).values(**task.dict()).returning(Task)
        )
        await self.session.commit()
        return dto.Task.model_validate(result.scalar())

    async def delete_one(self, task_id: int):
        await self.session.execute(delete(Task).where(Task.id == task_id))
        await self.session.commit()
