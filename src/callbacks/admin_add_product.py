from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
import uuid

from src.filters.is_admin import IsAdmin
from src.keyboards.builders import create_inline_keyboard
from src.schemas.product import Product
from src.services.service_product import ProductService
from src.states.add_product import AddProduct

admin_add_product = Router(name="Admin add product")
admin_add_product.message.filter(IsAdmin())


@admin_add_product.callback_query(F.data == "add_new_product")
async def start_add_new_product(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Введите ID категории")
    await state.set_state(AddProduct.category_id)


@admin_add_product.message(AddProduct.category_id, F.text)
async def get_product_category_id(message: Message, state: FSMContext):
    await state.update_data(category_id=message.text)
    await message.answer("Введите название товара")
    await state.set_state(AddProduct.name)


@admin_add_product.message(AddProduct.name, F.text)
async def get_product_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите описание товара")
    await state.set_state(AddProduct.description)


@admin_add_product.message(AddProduct.description, F.text)
async def get_product_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Введите стоимость товара (в звездах)")
    await state.set_state(AddProduct.price)


@admin_add_product.message(AddProduct.price, F.text)
async def get_product_description(message: Message, state: FSMContext):
    await state.update_data(price=message.text)

    data = await state.get_data()

    formatted_data = (
        "📋 <b>Проверьте данные:</b>\n\n"
        f"🆔 <b>ID категории:</b> <code>{data['category_id']}</code>\n"
        f"📛 <b>Название:</b> {data['name']}\n"
        f"📝 <b>Описание:</b> {data['description']}\n"
        f"💵 <b>Цена:</b> {data['price']} звёзд"
    )

    await message.answer(
        text=formatted_data,
        parse_mode="HTML",
        reply_markup=await create_inline_keyboard(
            [("✅ Добавить", "yes_add_product"),
             ("↩️ Главное меню", "back_to_main_menu")]
        )
    )


@admin_add_product.callback_query(F.data == "yes_add_product")
async def finish_add_new_product(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    await ProductService.add_new_product(
        Product(
            product_id=str(uuid.uuid4()),
            name=data["name"],
            description=data["description"],
            price=int(data["price"]),
            category_id=data["category_id"],
        )
    )
    await state.clear()

    await callback.message.answer("Успешно добавлено")
    await callback.answer()

