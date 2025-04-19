from aiogram.fsm.state import StatesGroup, State


class DeleteCategory(StatesGroup):
    category_id = State()
