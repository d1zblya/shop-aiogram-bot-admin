from typing import Optional

from sqlalchemy import Integer, String, BigInteger, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from src.database.session import Base


class ProductModel(Base):
    __tablename__ = 'products'

    product_id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(256), nullable=False)
    price: Mapped[Integer] = mapped_column(Integer, nullable=False)
    category_id: Mapped[Integer] = mapped_column(String, ForeignKey('categories.category_id'), nullable=False)

