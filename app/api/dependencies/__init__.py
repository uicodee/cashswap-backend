from aiogram import Bot
from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker

from app.api.dependencies.authentication import AuthProvider, get_user
from app.api.dependencies.bot import get_bot
from app.api.dependencies.database import DbProvider, dao_provider
from app.api.dependencies.settings import get_settings
from app.api.dependencies.telegram_auth import get_telegram_user, TelegramAuthProvider
from app.config import Settings, load_config


def setup(
    app: FastAPI,
    pool: sessionmaker,
    settings: Settings,
    bot: Bot
):
    db_provider = DbProvider(pool=pool)
    auth_provider = AuthProvider(settings=settings)
    telegram_auth_provider = TelegramAuthProvider(settings=settings)
    app.dependency_overrides[get_user] = auth_provider.get_current_user
    app.dependency_overrides[get_telegram_user] = (
        telegram_auth_provider.get_current_telegram_user
    )
    app.dependency_overrides[dao_provider] = db_provider.dao
    app.dependency_overrides[get_bot] = lambda: bot
    app.dependency_overrides[AuthProvider] = lambda: auth_provider
    app.dependency_overrides[get_settings] = load_config
