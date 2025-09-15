from aiogram import Router

from .menu import router as menu_router

router = Router()
router.include_routers(menu_router)

__all__ = ("router",)
