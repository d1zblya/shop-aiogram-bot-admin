from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
import uuid

from src.filters.is_admin import IsAdmin
from src.handlers.start import start_admin_handler
from src.keyboards.builders import create_inline_keyboard
from src.schemas.category import Category
from src.services.service_category import CategoryService
from src.states.add_category import AddCategory

admin_show_categories = Router(name="Admin show categories")
admin_show_categories.message.filter(IsAdmin())


@admin_show_categories.callback_query(F.data == "show_categories")
async def show_categories(callback: CallbackQuery):
    categories = await CategoryService.get_all_categories()

    lst_categories = [f"🗨{cat.title}\n🆔<code>{cat.category_id}</code>\n" for cat in categories]

    await callback.message.edit_text(
        text="\n".join(lst_categories),
        reply_markup=await create_inline_keyboard(
            [("🔙 Назад", "back_to_main_menu")]
        )
    )

    await callback.answer()
