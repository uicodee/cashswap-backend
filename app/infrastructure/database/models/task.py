from sqlalchemy import String, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.models import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .task_category import TaskCategory


class Task(BaseModel):
    __tablename__ = "task"

    title: Mapped[str] = mapped_column(String)
    reward: Mapped[float] = mapped_column(Numeric)
    link: Mapped[str] = mapped_column(String)

    category_id: Mapped[int] = mapped_column(
        ForeignKey("task_category.id", ondelete="CASCADE")
    )

    category: Mapped["TaskCategory"] = relationship(
        back_populates="tasks", lazy="selectin"
    )
