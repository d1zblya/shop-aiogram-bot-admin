from typing import Union

from src.database.dao.product_dao import ProductDAO
from src.database.session import async_session_maker
from loguru import logger

from src.exceptions.exceptions_product import CannotFindAllProducts, CannotAddProduct, CannotDeleteProduct
from src.schemas.product import Product


class ProductService:
    @classmethod
    async def get_all_products_by_category_id(cls, category_id: int) -> Union[list[Product], Product]:
        async with async_session_maker() as session:
            try:
                products = await ProductDAO.find_all(session, category_id=category_id)
                logger.success(f"Successfully found {len(products)} products")
                return products
            except Exception as e:
                msg = f"Cannot find all products: {str(e)}"
                logger.error(msg)
                raise CannotFindAllProducts(msg)

    @classmethod
    async def add_new_product(cls, product: Product):
        async with async_session_maker() as session:
            try:
                await ProductDAO.add(session, product)
                logger.success(f"Successfully added {product.name}")
                await session.commit()
            except Exception as e:
                msg = f"Cannot add {product.name}: {str(e)}"
                logger.error(msg)
                raise CannotAddProduct(msg)

    @classmethod
    async def get_all_products(cls) -> Union[list[Product], Product]:
        async with async_session_maker() as session:
            try:
                products = await ProductDAO.find_all(session)
                logger.success(f"Successfully found {len(products)} products")
                return products
            except Exception as e:
                msg = f"Cannot find all products: {str(e)}"
                logger.error(msg)
                raise CannotFindAllProducts(msg)

    @classmethod
    async def delete_product(cls, product_id: str):
        async with async_session_maker() as session:
            try:
                await ProductDAO.delete(session, product_id=product_id)
                await session.commit()
                logger.success(f"Successfully deleted {product_id}")
                return True
            except Exception as e:
                msg = f"Cannot delete {product_id}: {str(e)}"
                logger.error(msg)
                raise CannotDeleteProduct(msg)
