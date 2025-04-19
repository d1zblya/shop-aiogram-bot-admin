from aiogram.filters import Command
from aiogram import F, Router
from aiogram.types import Message, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from src.services.service_product import ProductService
from src.services.service_user import UserService
from src.utils.pagination import Pagination

admin_command_router = Router(name="Admin command router")


@admin_command_router.message(Command("users"))
async def admin_get_all_users(message: Message, state: FSMContext, is_edited: bool = False):
    await state.clear()

    users = await UserService.get_all_users()

    admin_users_pagination = Pagination(
        data=users,
        item_format=lambda user: f"{user.first_name} - {user.user_id}",
        item_callback=lambda user, prefix: f"{prefix}:{user.user_id}",
    )

    await state.update_data(admin_users_pagination=admin_users_pagination)
    await state.update_data(users=users)

    keyboard = await admin_users_pagination.get_page_keyboard(
        prefix="users",
        additional_buttons=[InlineKeyboardButton(text="Главное меню", callback_data="back_to_main_menu")],
    )

    if is_edited:
        await message.edit_text(f"👤 Список пользователей (всего {len(users)}):", reply_markup=keyboard)
        return
    await message.answer(f"👤 Список пользователей (всего {len(users)}):", reply_markup=keyboard)


@admin_command_router.message(Command("prods"))
async def admin_get_all_products(message: Message, state: FSMContext, is_edited: bool = False):
    await state.clear()

    products = await ProductService.get_all_products()

    admin_products_pagination = Pagination(
        data=products,
        item_format=lambda product: f"{product.name}",
        item_callback=lambda product, prefix: f"{prefix}:{product.product_id}",
        page_size=4
    )

    await state.update_data(admin_products_pagination=admin_products_pagination)
    await state.update_data(products=products)

    keyboard = await admin_products_pagination.get_page_keyboard(
        prefix="products",
        additional_buttons=[InlineKeyboardButton(text="Главное меню", callback_data="back_to_main_menu")],
    )

    if is_edited:
        await message.edit_text(f"® Список товаров (всего {len(products)}):", reply_markup=keyboard)
        return
    await message.answer(f"® Список товаров (всего {len(products)}):", reply_markup=keyboard)
