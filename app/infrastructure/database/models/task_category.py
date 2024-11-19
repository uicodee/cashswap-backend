from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.infrastructure.database.models import BaseModel
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .task import Task


class TaskCategory(BaseModel):
    __tablename__ = "task_category"

    name: Mapped[str] = mapped_column(String)
    icon: Mapped[str] = mapped_column(String)

    tasks: Mapped[List["Task"]] = relationship(back_populates="category")
