from typing import Optional

from sqlalchemy import Integer, String, BigInteger
from sqlalchemy.orm import mapped_column, Mapped

from src.database.session import Base


class CategoryModel(Base):
    __tablename__ = 'categories'

    category_id: Mapped[Integer] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)

