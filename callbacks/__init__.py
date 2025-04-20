from aiogram import Router
from .user import router as user_callbacks_router

router = Router(name="callbacks")

router.include_routers(
    user_callbacks_router
)

__all__ = ("router", )
