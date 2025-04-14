from pydantic import BaseModel, Field


class User(BaseModel):
    user_id: int = Field(..., alias='user_id')
    first_name: str = Field(..., alias='first_name')
    description: str = Field(default="Описание вашего профиля", alias='description')
