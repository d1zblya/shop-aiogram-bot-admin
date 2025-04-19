from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from aiogram.filters import CommandStart

from src.filters.is_admin import IsAdmin
from src.keyboards.inline import admin_main_kb
from src.schemas.user import User
from src.services.service_user import UserService

router = Router(name="Start router")


@router.message(CommandStart(), IsAdmin())
async def start_admin_handler(message: Message, is_edited: bool = False) -> None:
    """Обработчик команды /start для администратора"""
    if is_edited:
        await message.edit_text(
            text="🛠️ Админ-панель",
            reply_markup=admin_main_kb
        )
        return

    await message.answer(
        text="🛠️ Админ-панель",
        reply_markup=admin_main_kb
    )


@router.message(CommandStart())
async def start_user_handler(message: Message):
    await UserService.register_new_user(
        User(
            user_id=message.from_user.id,
            first_name=message.from_user.first_name,
        )
    )

    await message.answer(text=f"Привет, {message.from_user.first_name}!")


@router.callback_query(F.data == "back_to_main_menu", IsAdmin())
async def back_to_main_menu_callback_handler(callback: CallbackQuery):
    await start_admin_handler(callback.message, is_edited=True)
