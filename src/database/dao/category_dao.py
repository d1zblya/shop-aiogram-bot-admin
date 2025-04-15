from src.database.base_dao import BaseDAO
from src.database.models.category import CategoryModel
from src.schemas.category import Category


class CategoryDAO(BaseDAO[CategoryModel, Category]):
    model = CategoryModel
