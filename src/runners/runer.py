from aiogram import Bot, Dispatcher

from loguru import logger


async def on_startup(bot: Bot) -> None:
    logger.info("Bot started")
    pass


async def on_shutdown() -> None:
    pass


async def run_polling(dispatcher: Dispatcher, bot: Bot) -> None:
    dispatcher.startup.register(on_startup)
    dispatcher.shutdown.register(on_startup)
    return await dispatcher.start_polling(bot)
