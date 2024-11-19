from fastapi import APIRouter, Depends
from fastapi.params import Path
from pydantic import PositiveInt

from app import dto
from app.api import schems
from app.api.dependencies import dao_provider
from app.infrastructure.database import HolderDao

router = APIRouter(prefix="/task-category")


@router.post(
    path="/", response_model=dto.TaskCategory, description="Create a task category"
)
async def create_task_category(
    task_category: schems.TaskCategory, dao: HolderDao = Depends(dao_provider)
) -> dto.TaskCategory:
    return await dao.task_category.create(task_category=task_category)


@router.get(
    path="/", response_model=list[dto.TaskCategory], description="Get task categories"
)
async def get_task_categories(
    dao: HolderDao = Depends(dao_provider),
) -> list[dto.TaskCategory]:
    return await dao.task_category.get_all()


@router.get(
    path="/{task_category_id}",
    response_model=dto.TaskCategory,
    description="Get single task category",
)
async def get_task_category(
    task_category_id: PositiveInt = Path(),
) -> dto.TaskCategory: ...


@router.put(
    path="/{task_category_id}",
    response_model=dto.TaskCategory,
    description="Update task category",
)
async def update_task_category(
    task_category_id: PositiveInt = Path(),
) -> dto.TaskCategory: ...


@router.delete(
    path="/{task_category_id}",
    response_model=dto.TaskCategory,
    description="Delete task category",
)
async def delete_task_category(task_category_id: PositiveInt = Path()): ...
