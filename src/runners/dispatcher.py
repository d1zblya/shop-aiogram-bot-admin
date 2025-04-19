from aiogram import Dispatcher

from src.callbacks.admin_add_category import admin_add_category
from src.callbacks.admin_add_product import admin_add_product
from src.callbacks.admin_check_users import router as admin_check_users
from src.callbacks.admin_show_categories import admin_show_categories
from src.callbacks.admin_show_products import admin_show_products
from src.handlers.admin_commands import admin_command_router
from src.handlers.start import start_router


def _setup_outer_middlewares(dispatcher: Dispatcher) -> None:
    pass


def _setup_inner_middlewares(dispatcher: Dispatcher) -> None:
    pass


def _setup_routers(dispatcher: Dispatcher) -> None:
    dispatcher.include_routers(
        start_router,
        admin_check_users,
        admin_command_router,
        admin_add_category,
        admin_show_categories,
        admin_add_product,
        admin_show_products,
    )


async def create_dispatcher() -> Dispatcher:
    dispatcher: Dispatcher = Dispatcher(
        name="main_dispatcher",
    )

    _setup_routers(dispatcher=dispatcher)
    return dispatcher
