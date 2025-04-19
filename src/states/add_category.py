from aiogram.fsm.state import State, StatesGroup


class AddCategory(StatesGroup):
    title = State()
