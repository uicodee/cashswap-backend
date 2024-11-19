from sqlalchemy import String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.models import BaseModel


class Subscription(BaseModel):

    __tablename__ = "subscription"

    title: Mapped[int] = mapped_column(String)
    chat_id: Mapped[int] = mapped_column(BigInteger)
    link: Mapped[str] = mapped_column(String)
