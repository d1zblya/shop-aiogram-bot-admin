from pydantic import BaseModel, Field


class Product(BaseModel):
    product_id: str = Field(..., alias='product_id')
    name: str = Field(..., alias="name")
    description: str = Field(..., alias="description")
    price: int = Field(..., alias="price")
    category_id: str = Field(..., alias="category_id")
