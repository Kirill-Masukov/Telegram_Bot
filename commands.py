from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Запустить работу бота'
        ),
        BotCommand(
            command='help',
            description='Информация о работе бота'
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
