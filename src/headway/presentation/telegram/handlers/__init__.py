from aiogram import Router

from .menu import router as menu_router
from .commands import router as commands_router

router = Router()
router.include_routers(menu_router, commands_router)

__all__ = ("router",)
