from pydantic import BaseModel, Field


class UpdateTelegramUser(BaseModel):

    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")
    username: str
    balance: float
