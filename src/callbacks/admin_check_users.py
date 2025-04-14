from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from src.schemas.user import User

admin_check_users = Router(name="Admin check users")


@admin_check_users.callback_query(F.data.startswith("users:"), F.data.split(":")[1].isdigit())
async def show_product_details(callback: CallbackQuery, state: FSMContext):
    admin_users_pagination = await state.get_value("admin_users_pagination")
    users = await state.get_value("users")

    user_id = int(callback.data.split(":")[1])
    user: User = next((user for user in users if user.user_id == user_id), None)

    if not user:
        await callback.answer("Пользователь не найден!", show_alert=True)
        return

    # Клавиатура с действиями
    buttons = [
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_users_list")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await state.update_data(admin_users_pagination=admin_users_pagination)

    await callback.message.edit_text(
        f"<b>{user.first_name}</b>\n\n"
        f"🆔 ID: <code>{user.user_id}</code>\n"
        f"📝 Описание: <i>{user.description}</i>",
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    await callback.answer()


@admin_check_users.callback_query(
    F.data.startswith("users:"),
    lambda query: query.data.split(":")[1] in ("prev", "next")
)
async def handle_pagination(callback: CallbackQuery, state: FSMContext):
    admin_users_pagination = await state.get_value("admin_users_pagination")

    action = callback.data.split(":")[1]

    if action in ("prev", "next"):
        old_page = admin_users_pagination.current_page
        new_page = await admin_users_pagination.process_callback(callback.data)

        # Если страница не изменилась - просто выходим
        if old_page == new_page:
            await callback.answer()
            return

        keyboard = await admin_users_pagination.get_page_keyboard(prefix="users")

        await state.update_data(admin_users_pagination=admin_users_pagination)

        try:
            await callback.message.edit_text(
                "👤 Список пользователей:",
                reply_markup=keyboard
            )
        except TelegramBadRequest as e:
            if "message is not modified" in str(e):
                await callback.answer()
            else:
                raise

        await callback.answer()


@admin_check_users.callback_query(F.data == "back_to_users_list")
async def back_to_users_list(callback: CallbackQuery, state: FSMContext):
    admin_users_pagination = await state.get_value("admin_users_pagination")

    keyboard = await admin_users_pagination.get_page_keyboard(prefix="users")
    await callback.message.edit_text("👤 Список пользователей:", reply_markup=keyboard)
