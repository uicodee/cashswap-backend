from pydantic import Field, BaseModel, PositiveInt


class Task(BaseModel):
    title: str
    reward: float
    link: str
    category_id: int = Field(alias="categoryId")


class DeleteTask(BaseModel):
    skills_ids: list[PositiveInt] = Field(alias="taskIds")
