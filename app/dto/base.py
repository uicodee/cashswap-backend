from datetime import datetime

from pydantic import BaseModel as PydanticBaseModel, Field


def serialize_time(value: datetime) -> int:
    return int(value.timestamp())


class BasePydanticModel(PydanticBaseModel):
    class Config:
        from_attributes = True
        populate_by_name = True


class Base(BasePydanticModel):
    id: int


class BaseModel(Base):
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")

    class Config:
        json_encoders = {datetime: serialize_time}


class BaseWithDateOnly(BasePydanticModel):
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")

    class Config:
        json_encoders = {datetime: serialize_time}
