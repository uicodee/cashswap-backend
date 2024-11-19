from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.models import BaseModel


class CompletedTask(BaseModel):

    __tablename__ = "completed_task"

    task_id: Mapped[int] = mapped_column(ForeignKey("task.id", ondelete="CASCADE"))
    telegram_user_id: Mapped[int] = mapped_column(
        ForeignKey("telegram_user.telegram_id", ondelete="CASCADE")
    )
