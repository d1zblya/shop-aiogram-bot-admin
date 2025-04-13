from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from src.core.config import settings


async def _set_default_commands(bot: Bot) -> None:
    user_commands = [BotCommand(command="start", description="Запустить бота")]
    await bot.set_my_commands(user_commands)


async def create_bot() -> Bot:
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
        ),
    )
    await _set_default_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    return bot
