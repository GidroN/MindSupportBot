from aiogram import Router
from callbacks import router as callback_router
from handlers import router as handlers_router

router = Router(name="main")

router.include_routers(
    callback_router,
    handlers_router
)

__all__ = ("router", )
