from typing import Optional

from sqlalchemy import Integer, String, BigInteger
from sqlalchemy.orm import mapped_column, Mapped

from src.database.session import Base


class UserModel(Base):
    __tablename__ = 'users'

    user_id: Mapped[BigInteger] = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, default="Описание вашего профиля")
