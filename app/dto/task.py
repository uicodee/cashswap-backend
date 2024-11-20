from pydantic import Field

from app.dto import BaseModel
from .task_category import TaskCategory


class Task(BaseModel):
    title: str
    reward: float
    link: str
    chat_id: int = Field(alias="chatId")
    category: TaskCategory
