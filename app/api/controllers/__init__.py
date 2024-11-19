from fastapi import FastAPI

from .authentication import router as authentication_router
from .task import router as task_router
from .task_category import router as task_category_router
from .telegram_user import router as telegram_user_router
from .subscription import router as subscription_router


def setup(app: FastAPI) -> None:
    app.include_router(router=authentication_router, tags=["Authentication"])
    app.include_router(router=telegram_user_router, tags=["Telegram User"])
    app.include_router(router=task_router, tags=["Task"])
    app.include_router(router=task_category_router, tags=["Task Category"])
    app.include_router(router=subscription_router, tags=["Subscription"])
