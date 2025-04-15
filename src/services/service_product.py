from src.database.dao.product_dao import ProductDAO
from src.database.session import async_session_maker
from loguru import logger

from src.exceptions.exceptions_product import CannotFindAllProducts


class ProductService:
    @classmethod
    async def get_all_products_by_category_id(cls, category_id: int):
        async with async_session_maker() as session:
            try:
                products = await ProductDAO.find_all(session, category_id=category_id)
                logger.success(f"Successfully found {len(products)} products")
                return products
            except Exception as e:
                msg = f"Cannot find all products: {str(e)}"
                logger.error(msg)
                raise CannotFindAllProducts(msg)
