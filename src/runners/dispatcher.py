from aiogram import Dispatcher

from src.handlers.start import start_router


def _setup_outer_middlewares(dispatcher: Dispatcher) -> None:
    pass


def _setup_inner_middlewares(dispatcher: Dispatcher) -> None:
    pass


def _setup_routers(dispatcher: Dispatcher) -> None:
    dispatcher.include_routers(
        start_router
    )


async def create_dispatcher() -> Dispatcher:
    dispatcher: Dispatcher = Dispatcher(
        name="main_dispatcher",
    )

    _setup_routers(dispatcher=dispatcher)
    return dispatcher
