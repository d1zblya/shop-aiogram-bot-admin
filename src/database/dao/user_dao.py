from src.database.base_dao import BaseDAO
from src.database.models.user import UserModel
from src.schemas.user import User


class UserDAO(BaseDAO[UserModel, User]):
    model = UserModel
