from pydantic import Field, BaseModel


class Task(BaseModel):
    title: str
    reward: float
    link: str
    category_id: int = Field(alias="categoryId")
