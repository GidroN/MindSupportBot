from aiogram import Router

from .add_post_form import router as add_post_form_router
from .message_user_form import router as message_user_form_router
from .register_user_form import router as register_user_form_router
from .send_newsletter_form import router as send_newsletter_form_router

router = Router(name="user_state_handlers")

router.include_routers(
    add_post_form_router,
    message_user_form_router,
    register_user_form_router,
    send_newsletter_form_router
)

__all__ = ("router", )
