from pydantic import BaseModel, Field


class Category(BaseModel):
    category_id: int = Field(..., alias="category_id")
    title: str = Field(..., alias="title")
