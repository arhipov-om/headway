from aiogram import Router

from .create_reminder import router as reminders_router
from .menu import router as menu_router

router = Router()
router.include_routers(menu_router, reminders_router)

__all__ = ("router",)
