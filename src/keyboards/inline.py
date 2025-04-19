from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

admin_main_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Добавить категорию", callback_data="add_new_category"),
         InlineKeyboardButton(text="Добавить товар", callback_data="add_new_product")],
        [InlineKeyboardButton(text="Просмотреть категории", callback_data="show_categories"),
         InlineKeyboardButton(text="Просмотреть товары", callback_data="show_products")],
        [InlineKeyboardButton(text="Пользователи", callback_data="users"),]
    ]
)
