from src.database.dao.category_dao import CategoryDAO
from src.database.session import async_session_maker
from loguru import logger

from src.exceptions.exceptions_category import CannotFindAllCategories, CannotAddCategory
from src.schemas.category import Category


class CategoryService:
    @classmethod
    async def get_all_categories(cls):
        async with async_session_maker() as session:
            try:
                categories = await CategoryDAO.find_all(session)
                logger.success(f"Successfully found {len(categories)} categories")
                return categories
            except Exception as e:
                msg = f"Cannot find all categories: {str(e)}"
                logger.error(msg)
                raise CannotFindAllCategories(msg)

    @classmethod
    async def add_new_category(cls, category: Category):
        async with async_session_maker() as session:
            try:
                await CategoryDAO.add(session, category)
                logger.success(f"Successfully added {category.name}")
            except Exception as e:
                msg = f"Cannot add {category.name}: {str(e)}"
                logger.error(msg)
                raise CannotAddCategory(msg)
