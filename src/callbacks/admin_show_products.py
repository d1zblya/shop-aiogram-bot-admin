from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from src.handlers.admin_commands import admin_get_all_users, admin_get_all_products
from src.schemas.product import Product
from src.schemas.user import User
import re


def is_uuid(uuid_str: str) -> bool:
    pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    return bool(re.fullmatch(pattern, uuid_str, flags=re.IGNORECASE))


admin_show_products = Router(name="Admin show products")


@admin_show_products.callback_query(F.data == "show_products")
async def admin_get_products_before_main_menu(callback: CallbackQuery, state: FSMContext):
    await admin_get_all_products(message=callback.message, state=state, is_edited=True)


@admin_show_products.callback_query(
    F.data.startswith("products:"),
    lambda query: is_uuid(query.data.split(":")[1])  # Проверяем вторую часть на UUID
)
async def show_product_details(callback: CallbackQuery, state: FSMContext):
    admin_products_pagination = await state.get_value("admin_products_pagination")
    products = await state.get_value("products")

    product_id = str(callback.data.split(":")[1])
    product: Product = next((product for product in products if product.product_id == product_id), None)

    if not product:
        await callback.answer("Товар не найден!", show_alert=True)
        return

    # Клавиатура с действиями
    buttons = [
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_products_list")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await state.update_data(admin_products_pagination=admin_products_pagination)

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


@admin_show_products.callback_query(
    F.data.startswith("products:"),
    lambda query: query.data.split(":")[1] in ("prev", "next")
)
async def handle_pagination(callback: CallbackQuery, state: FSMContext):
    admin_products_pagination = await state.get_value("admin_products_pagination")
    products = await state.get_value("products")

    action = callback.data.split(":")[1]

    if action in ("prev", "next"):
        old_page = admin_products_pagination.current_page
        new_page = await admin_products_pagination.process_callback(callback.data)

        # Если страница не изменилась - просто выходим
        if old_page == new_page:
            await callback.answer()
            return

        keyboard = await admin_products_pagination.get_page_keyboard(
            prefix="products",
            additional_buttons=[InlineKeyboardButton(text="Главное меню", callback_data="back_to_main_menu")],
        )

        await state.update_data(admin_products_pagination=admin_products_pagination)

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


@admin_show_products.callback_query(F.data == "back_to_products_list")
async def back_to_users_list(callback: CallbackQuery, state: FSMContext):
    admin_products_pagination = await state.get_value("admin_products_pagination")
    products = await state.get_value("products")

    keyboard = await admin_products_pagination.get_page_keyboard(
        prefix="products",
        additional_buttons=[InlineKeyboardButton(text="Главное меню", callback_data="back_to_main_menu")],
    )
    await callback.message.edit_text(f"® Список товаров (всего {len(products)}):", reply_markup=keyboard)
