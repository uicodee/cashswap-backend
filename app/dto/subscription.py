from pydantic import Field

from app.dto import BaseModel


class Subscription(BaseModel):
    title: str
    chat_id: int = Field(alias="chatId")
    link: str
