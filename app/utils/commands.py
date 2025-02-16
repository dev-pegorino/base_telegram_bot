from aiogram.types import BotCommand

from app.utils.strings import commands


async def commands_():
    bot_commands = []
    for command in commands:
        bot_commands.append(BotCommand(command=command[0], description=command[1]))
    return bot_commands
