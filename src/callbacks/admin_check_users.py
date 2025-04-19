from typing import Union

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from src.handlers.admin_commands import admin_get_all_users
from src.schemas.user import User

router = Router(name="Admin check users")


async def _get_user_from_state(callback: CallbackQuery, state: FSMContext) -> Union[User, None]:
    """Получает пользователя из state по ID из callback данных"""
    user_id = int(callback.data.split(":")[1])
    users = await state.get_value("users")
    return next((user for user in users if user.user_id == user_id), None)


@router.callback_query(F.data == "users")
async def handle_users_list_request(callback: CallbackQuery, state: FSMContext):
    """Обработчик запроса списка пользователей"""
    await admin_get_all_users(message=callback.message, state=state, is_edited=True)


@router.callback_query(F.data.startswith("users:"), F.data.split(":")[1].isdigit())
async def show_user_details(callback: CallbackQuery, state: FSMContext):
    """Показывает детали конкретного пользователя"""
    user = await _get_user_from_state(callback, state)
    if not user:
        await callback.answer("Пользователь не найден!", show_alert=True)
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_users_list")]]
    )

    await callback.message.edit_text(
        f"<b>{user.first_name}</b>\n\n"
        f"🆔 ID: <code>{user.user_id}</code>\n"
        f"📝 Описание: <i>{user.description}</i>",
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(
    F.data.startswith("users:"),
    lambda query: query.data.split(":")[1] in ("prev", "next")
)
async def handle_users_pagination(callback: CallbackQuery, state: FSMContext):
    """Обработчик пагинации списка пользователей"""
    pagination = await state.get_value("admin_users_pagination")
    users = await state.get_value("users")

    action = callback.data.split(":")[1]

    if action in ("prev", "next"):
        old_page = pagination.current_page
        new_page = await pagination.process_callback(callback.data)

        # Если страница не изменилась - просто выходим
        if old_page == new_page:
            await callback.answer()
            return

        keyboard = await pagination.get_page_keyboard(
            prefix="users",
            additional_buttons=[InlineKeyboardButton(text="Главное меню", callback_data="back_to_main_menu")],
        )

        await state.update_data(admin_users_pagination=pagination)

        try:
            await callback.message.edit_text(
                f"👤 Список пользователей (всего {len(users)}):",
                reply_markup=keyboard
            )
        except TelegramBadRequest as e:
            if "message is not modified" in str(e):
                await callback.answer()
            else:
                raise

        await callback.answer()


@router.callback_query(F.data == "back_to_users_list")
async def return_to_users_list(callback: CallbackQuery, state: FSMContext):
    """Возврат к списку пользователей"""
    admin_users_pagination = await state.get_value("admin_users_pagination")
    users = await state.get_value("users")

    keyboard = await admin_users_pagination.get_page_keyboard(
        prefix="users",
        additional_buttons=[InlineKeyboardButton(text="Главное меню", callback_data="back_to_main_menu")],
    )
    await callback.message.edit_text(f"👤 Список пользователей (всего {len(users)}):", reply_markup=keyboard)
