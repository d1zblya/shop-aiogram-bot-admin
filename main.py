import asyncio
from typing import TYPE_CHECKING

from src.core.logger import setup_logger
from src.runners.bot import create_bot
from src.runners.dispatcher import create_dispatcher
from src.runners.runer import run_polling

if TYPE_CHECKING:
    from aiogram import Bot, Dispatcher

from loguru import logger


async def main() -> None:
    setup_logger()

    dispatcher: Dispatcher = await create_dispatcher()
    bot: Bot = await create_bot()

    return await run_polling(dispatcher=dispatcher, bot=bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Stopping bot")
