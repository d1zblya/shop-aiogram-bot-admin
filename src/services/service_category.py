from src.database.dao.category_dao import CategoryDAO
from src.database.session import async_session_maker
from loguru import logger

from src.exceptions.exceptions_category import CannotFindAllCategories, CannotAddCategory, CannroDeleteCategory
from src.schemas.category import Category


class CategoryService:
    @classmethod
    async def get_all_categories(cls) -> list[Category]:
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
                logger.success(f"Successfully added {category.title}")
                await session.commit()
            except Exception as e:
                msg = f"Cannot add {category.title}: {str(e)}"
                logger.error(msg)
                raise CannotAddCategory(msg)

    @classmethod
    async def delete_category(cls, category_id: str):
        async with async_session_maker() as session:
            try:
                await CategoryDAO.delete(session, category_id=category_id)
                logger.success(f"Successfully deleted {category_id}")
                await session.commit()
                return True
            except Exception as e:
                msg = f"Cannot delete {category_id}: {str(e)}"
                logger.error(msg)
                raise CannroDeleteCategory(msg)
