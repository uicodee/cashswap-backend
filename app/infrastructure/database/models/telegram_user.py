from datetime import datetime, timedelta

from sqlalchemy import BigInteger, String, Numeric, DateTime, func, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.sql import expression

from app.infrastructure.database.models import BaseWithDateOnly


class TelegramUser(BaseWithDateOnly):
    __tablename__ = "telegram_user"

    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=True)
    first_name: Mapped[str] = mapped_column(String, nullable=True)
    last_name: Mapped[str] = mapped_column(String, nullable=True)
    balance: Mapped[float] = mapped_column(Numeric, default=0.0)
    extra_balance: Mapped[float] = mapped_column(Numeric, default=0.0)

    last_farm: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=True
    )
    next_farm: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=expression.text("(NOW() + INTERVAL '8 hours')"),
    )

    referrer_id: Mapped[int] = mapped_column(
        ForeignKey("telegram_user.telegram_id", ondelete="CASCADE"), nullable=True
    )
    referrals: Mapped[int] = mapped_column(BigInteger, default=0)
    tickets: Mapped[int] = mapped_column(BigInteger, default=0)
    days_active: Mapped[int] = mapped_column(BigInteger, default=1)
    last_days_active: Mapped[int] = mapped_column(BigInteger, default=0)
    last_action: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=True
    )
    last_daily_reward: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
