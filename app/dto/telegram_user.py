from datetime import datetime
from pydantic import Field, BaseModel as PydanticBaseModel

from app.dto import BaseWithDateOnly


class TelegramUser(BaseWithDateOnly):
    telegram_id: int = Field(alias="telegramId")
    username: str | None = Field(default=None)
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")
    balance: float = Field()
    extra_balance: float = Field(alias="extraBalance")
    last_farm: datetime | None = Field(default=None, alias="lastFarm")
    next_farm: datetime = Field(alias="nextFarm")
    place: int | None = Field(default=None)
    already_farmed: float | None = Field(default=None, alias="alreadyFarmed")
    percent: int | None = Field(default=None)
    referrer_id: int | None = Field(alias="referrerId")
    referrals: int = Field(default=0)
    tickets: int = Field(default=0)
    days_active: int = Field(default=1, alias="daysActive")
    last_days_active: int = Field(default=1, alias="lastDaysActive")
    last_action: datetime = Field(last_action="lastAction")
    last_daily_reward: datetime | None = Field(default=None, alias="lastDailyReward")


class Rating(PydanticBaseModel):
    place: int
