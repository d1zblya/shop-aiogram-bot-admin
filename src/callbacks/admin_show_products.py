from typing import Union
from uuid import UUID

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from src.handlers.admin_commands import admin_get_all_users, admin_get_all_products
from src.schemas.product import Product
from src.schemas.user import User
import re


def _is_valid_uuid(uuid_str: str) -> bool:
    """Проверяет, является ли строка валидным UUID"""
    try:
        UUID(uuid_str)
        return True
    except ValueError:
        return False


async def _get_product_from_state(callback: CallbackQuery, state: FSMContext) -> Union[Product, None]:
    """Получает товар из state по ID из callback данных"""
    product_id = callback.data.split(":")[1]
    products = await state.get_value("products")
    return next((product for product in products if product.product_id == product_id), None)


router = Router(name="Admin show products")


@router.callback_query(F.data == "show_products")
async def handle_products_list_request(callback: CallbackQuery, state: FSMContext):
    """Обработчик запроса списка товаров"""
    await admin_get_all_products(message=callback.message, state=state, is_edited=True)


@router.callback_query(
    F.data.startswith("products:"),
    lambda query: _is_valid_uuid(query.data.split(":")[1])
)
async def show_product_details(callback: CallbackQuery, state: FSMContext):
    """Показывает детали конкретного товара"""
    product = await _get_product_from_state(callback, state)
    if not product:
        await callback.answer("Товар не найден!", show_alert=True)
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_products_list")]]
    )

    await callback.message.edit_text(
        "🛍️ <b>Данные товара</b>\n"
        f"├─ 🆔 <code>{product.product_id}</code>\n"
        f"├─ 📛 {product.name}\n"
        f"├─ 💰 {product.price} звёзд\n"
        f"└─ 🗂 Кат.: <code>{product.category_id}</code>\n\n"
        f"📄 <b>Описание:</b>\n<i>{product.description}</i>",
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(
    F.data.startswith("products:"),
    lambda query: query.data.split(":")[1] in ("prev", "next")
)
async def handle_products_pagination(callback: CallbackQuery, state: FSMContext):
    """Обработчик пагинации списка товаров"""
    pagination = await state.get_value("admin_products_pagination")
    products = await state.get_value("products")
    old_page = pagination.current_page
    new_page = await pagination.process_callback(callback.data)

    if old_page == new_page:
        await callback.answer()
        return

    keyboard = await pagination.get_page_keyboard(
        prefix="products",
        additional_buttons=[InlineKeyboardButton(text="Главное меню", callback_data="back_to_main_menu")],
    )

    await state.update_data(admin_products_pagination=pagination)

    try:
        await callback.message.edit_text(
            f"® Список товаров (всего {len(products)}):",
            reply_markup=keyboard
        )
    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            await callback.answer()
        else:
            raise

    await callback.answer()


@router.callback_query(F.data == "back_to_products_list")
async def return_to_products_list(callback: CallbackQuery, state: FSMContext):
    """Возврат к списку товаров"""
    pagination = await state.get_value("admin_products_pagination")
    products = await state.get_value("products")

    keyboard = await pagination.get_page_keyboard(
        prefix="products",
        additional_buttons=[InlineKeyboardButton(text="Главное меню", callback_data="back_to_main_menu")],
    )
    await callback.message.edit_text(f"® Список товаров (всего {len(products)}):", reply_markup=keyboard)
