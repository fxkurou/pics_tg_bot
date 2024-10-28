from aiogram import Router

from bot.handlers.start import start_router
from bot.handlers.admin.load_pic import load_pic_router
from bot.handlers.gallery import gallery_router
from bot.handlers.donate import donate_router

main_router = Router()

main_router.include_router(start_router)
main_router.include_router(load_pic_router)
main_router.include_router(gallery_router)
main_router.include_router(donate_router)