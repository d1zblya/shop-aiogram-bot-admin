from aiogram.filters import Command
from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from src.services.service_user import UserService
from src.utils.pagination import Pagination

admin_command_router = Router(name="Admin command router")


@admin_command_router.message(Command("users"))
async def admin_get_all_users(message: Message, state: FSMContext):
    await state.clear()

    users = await UserService.get_all_users()

    admin_users_pagination = Pagination(
        data=users,
        item_format=lambda user: f"{user.first_name} - {user.user_id}",
        item_callback=lambda user, prefix: f"{prefix}:{user.user_id}",
    )

    await state.update_data(admin_users_pagination=admin_users_pagination)
    await state.update_data(users=users)

    keyboard = await admin_users_pagination.get_page_keyboard(prefix="users")
    await message.answer(f"👤 Список пользователей (всего {len(users)}):", reply_markup=keyboard)
