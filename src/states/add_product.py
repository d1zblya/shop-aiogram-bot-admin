from aiogram.fsm.state import StatesGroup, State


class AddProduct(StatesGroup):
    category_id = State()
    name = State()
    description = State()
    price = State()
