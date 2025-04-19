from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
import uuid

from src.filters.is_admin import IsAdmin
from src.handlers.start import start_admin_handler
from src.schemas.category import Category
from src.services.service_category import CategoryService
from src.states.add_category import AddCategory

admin_add_category = Router(name="Admin add category")
admin_add_category.message.filter(IsAdmin())


@admin_add_category.callback_query(F.data == "add_new_category")
async def title_category(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Введите название категории")
    await state.set_state(AddCategory.title)


@admin_add_category.message(AddCategory.title, F.text)
async def add_category_in_db(message: Message, state: FSMContext):
    title = str(message.text).capitalize()
    await CategoryService.add_new_category(
        Category(
            category_id=str(uuid.uuid4()),
            title=title,
        )
    )

    await state.clear()

    await message.answer(f"{title} - успешно добавлено")

    await start_admin_handler(message)


