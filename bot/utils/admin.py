# from aiogram import Bot
# from aiogram.types import Message
# from aiogram.enums import ChatMemberStatus
#
# async def is_admin(user_id: int, chat_id: int, bot: Bot):
#     """
#     Check if a user is an admin in the current chat.
#     """
#     member = await bot.get_chat_member(chat_id, user_id)
#     return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]
#
#
# def admin_or_creator_only(func):
#     """
#     Decorator to restrict access to admins or the chat creator only.
#     """
#     async def wrapper(message: Message, *args, **kwargs):
#         user_id = message.from_user.id
#         chat_id = message.chat.id
#         if not await is_admin(user_id, chat_id, message.bot):
#             await message.reply("You are not authorized to upload pictures.")
#             return
#         return await func(message, *args, **kwargs)
#     return wrapper