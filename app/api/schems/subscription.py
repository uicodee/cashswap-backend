from pydantic import BaseModel, Field


class Subscription(BaseModel):
    title: str
    chat_id: int = Field(alias="chatId")
    link: str
