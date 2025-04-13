from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from aiogram.filters import CommandStart

from src.filters.is_admin import IsAdmin

start_router = Router(name="Start router")


@start_router.message(CommandStart(), IsAdmin())
async def start_admin_handler(message: Message):
    await message.answer(text="Привет, Админ!")


@start_router.message(CommandStart())
async def start_user_handler(message: Message):
    await message.answer(text=f"Привет, {message.from_user.first_name}!")
