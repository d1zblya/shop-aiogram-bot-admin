from src.database.base_dao import BaseDAO
from src.database.models.product import ProductModel
from src.schemas.product import Product


class ProductDAO(BaseDAO[ProductModel, Product]):
    model = ProductModel
