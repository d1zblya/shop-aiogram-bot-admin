from src.database.dao.user_dao import UserDAO
from src.database.session import async_session_maker
from src.exceptions.exceptions_user import ErrorUserRegister
from src.schemas.user import User

from loguru import logger


class UserService:
    @classmethod
    async def register_new_user(cls, user: User):
        async with async_session_maker() as session:
            try:
                exists_user = await UserDAO.find_one_or_none(session, user_id=user.user_id)
                if exists_user is None:
                    user = await UserDAO.add(session, user)
                    await session.commit()
                    logger.success("User successfully registered")
                    return user

                logger.info("User already registered")
                return exists_user

            except Exception as e:
                msg = f"Error in user registration: {str(e)}"
                logger.error(msg)
                raise ErrorUserRegister(msg)
