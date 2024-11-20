from aiogram import Bot
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.params import Path
from pydantic import PositiveInt

from app import dto
from app.api import schems
from app.api.dependencies import dao_provider, get_telegram_user, get_user, get_bot
from app.infrastructure.database import HolderDao

router = APIRouter(prefix="/task")


@router.post(path="/", response_model=dto.Task, description="Create a task", dependencies=[Depends(get_user)])
async def create_task(
        task: schems.Task, dao: HolderDao = Depends(dao_provider)
) -> dto.Task:
    return await dao.task.create(task=task)


@router.get(path="/", response_model=list[dto.Task], description="Get tasks")
async def get_tasks(dao: HolderDao = Depends(dao_provider)) -> list[dto.Task]:
    return await dao.task.get_all()


@router.get(
    path="/user-tasks", response_model=list[dto.Task], description="Get user tasks"
)
async def get_user_tasks(
        telegram_user: dto.TelegramUser = Depends(get_telegram_user),
        dao: HolderDao = Depends(dao_provider),
) -> list[dto.Task]:
    tasks_ids = await dao.task.get_completed_tasks(
        telegram_user_id=telegram_user.telegram_id
    )
    tasks = await dao.task.get_all()
    user_tasks = []
    for task in tasks:
        if task.id not in tasks_ids:
            user_tasks.append(task)
    return user_tasks


@router.post(path="/check/{task_id}", description="Get task status")
async def get_task_status(
        task_id: PositiveInt = Path(),
        bot: Bot = Depends(get_bot),
        telegram_user: dto.TelegramUser = Depends(get_telegram_user),
        dao: HolderDao = Depends(dao_provider),
) -> JSONResponse:
    tasks_ids = await dao.task.get_completed_tasks(
        telegram_user_id=telegram_user.telegram_id
    )
    task = await dao.task.get_one(task_id=task_id)
    if task.id in tasks_ids:
        return JSONResponse(status_code=200, content={"status": "Success"})
    else:
        task_category = await dao.task_category.get_one(
            task_category_id=task.category.id
        )
        if task_category.name == "Telegram":
            current_status = await bot.get_chat_member(
                chat_id=task.link,
                user_id=telegram_user.telegram_id
            )
            if current_status.status == "left":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Task is not completed"
                )
            else:
                return JSONResponse(status_code=200, content={"status": "Success"})
        else:
            await dao.telegram_user.update_user_balance(
                telegram_id=telegram_user.telegram_id,
                balance=telegram_user.balance + task.reward,
            )
            await dao.task.create_completed_task(
                task_id=task_id, telegram_user_id=telegram_user.telegram_id
            )
            return JSONResponse(status_code=200, content={"status": "Success"})


@router.get(path="/{task_id}", response_model=dto.Task, description="Get single task")
async def get_task(
        dao: HolderDao = Depends(dao_provider), task_id: PositiveInt = Path()
) -> dto.Task:
    current_task = await dao.task.get_one(task_id=task_id)
    if current_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return current_task


@router.put(path="/{task_id}", response_model=dto.Task, description="Update task", dependencies=[Depends(get_user)])
async def update_task(
        task: schems.Task,
        dao: HolderDao = Depends(dao_provider),
        task_id: PositiveInt = Path(),
) -> dto.Task:
    current_task = await dao.task.get_one(task_id=task_id)
    if current_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return await dao.task.update_one(task_id=task_id, task=task)


@router.delete(path="/", description="Delete task", dependencies=[Depends(get_user)])
async def delete_task(
        tasks: schems.DeleteTask,
        dao: HolderDao = Depends(dao_provider)
):
    for task in tasks:
        current_task = await dao.task.get_one(task_id=task)
        if current_task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
            )
        await dao.task.delete_one(task_id=task)
