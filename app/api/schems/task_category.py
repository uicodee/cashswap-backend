from pydantic import BaseModel


class TaskCategory(BaseModel):
    name: str
    icon: str
