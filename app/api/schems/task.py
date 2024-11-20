from pydantic import Field, BaseModel, PositiveInt


class Task(BaseModel):
    title: str
    reward: float
    link: str
    chat_id: int = Field(alias="chatId")
    category_id: int = Field(alias="categoryId")


class DeleteTask(BaseModel):
    task_ids: list[PositiveInt] = Field(alias="taskIds")
