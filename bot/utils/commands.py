# from aiogram import Bot
# from aiogram.types import BotCommandScopeDefault, BotCommand
#
#
# async def set_commands(bot: Bot):
#     commands = [
#         BotCommand(
#             command='/start',
#             description='Start the bot'
#         ),
#         BotCommand(
#             command='/gallery',
#             description='Show gallery'
#         ),
#         BotCommand(
#             command='/search',
#             description='Search pic by tag'
#         ),
#         BotCommand(
#             command='/upload_pic',
#             description='Add pics to gallery'
#         ),
#         BotCommand(
#             command='/help',
#             description='Show help message'
#         ),
#     ]
#
#     await bot.set_my_commands(commands, scope=BotCommandScopeDefault())
