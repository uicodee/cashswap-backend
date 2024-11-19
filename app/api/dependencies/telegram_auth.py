from datetime import datetime, timedelta, timezone
from typing import Annotated

from aiogram.utils.web_app import check_webapp_signature, safe_parse_webapp_init_data
from fastapi import Request, HTTPException, status, Depends, Header

from app import dto
from app.api.dependencies.database import dao_provider
from app.config import Settings
from app.infrastructure.database import HolderDao


def get_telegram_user(
    authorization: Annotated[list[str] | None, Header(alias="Authorization")] = None
) -> dto.TelegramUser:
    raise NotImplementedError


class TelegramAuthProvider:

    def __init__(self, settings: Settings):
        self.settings = settings

    async def get_current_telegram_user(
        self, request: Request, dao: HolderDao = Depends(dao_provider)
    ) -> dto.TelegramUser:
        telegram_init_data = request.headers.get("Authorization")
        unauthorized_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )
        bad_request_exception = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Unregistered"
        )
        if telegram_init_data is None:
            raise unauthorized_exception
        if not check_webapp_signature(self.settings.tgbot.token, telegram_init_data):
            raise unauthorized_exception
        web_app_init_data = safe_parse_webapp_init_data(
            token=self.settings.tgbot.token, init_data=telegram_init_data
        )
        telegram_user = await dao.telegram_user.get_telegram_user(
            telegram_id=web_app_init_data.user.id
        )
        if telegram_user is None:
            referrer_id = request.headers.get("X-Referrer-Id")
            if referrer_id is not None:
                referrer = await dao.telegram_user.get_telegram_user(
                    telegram_id=int(referrer_id)
                )
                if referrer is not None:
                    created_user = await dao.telegram_user.create(
                        telegram_id=web_app_init_data.user.id,
                        username=web_app_init_data.user.username,
                        first_name=web_app_init_data.user.first_name,
                        last_name=web_app_init_data.user.last_name,
                        referrer_id=int(referrer_id),
                    )
                    await dao.telegram_user.update_referrals(
                        telegram_id=int(referrer_id),
                        tickets=referrer.tickets + 1,
                        referrals=referrer.referrals + 1,
                        balance=referrer.balance + 100,
                    )
                    return created_user
                else:
                    return await dao.telegram_user.create(
                        telegram_id=web_app_init_data.user.id,
                        username=web_app_init_data.user.username,
                        first_name=web_app_init_data.user.first_name,
                        last_name=web_app_init_data.user.last_name,
                    )
            else:
                return await dao.telegram_user.create(
                    telegram_id=web_app_init_data.user.id,
                    username=web_app_init_data.user.username,
                    first_name=web_app_init_data.user.first_name,
                    last_name=web_app_init_data.user.last_name,
                )
        else:
            now = datetime.now()
            last_action_date = telegram_user.last_action.astimezone(
                tz=timezone(timedelta(hours=3))
            ).date()
            yesterday_date = (
                (now - timedelta(days=1))
                .astimezone(tz=timezone(timedelta(hours=3)))
                .date()
            )

            if (yesterday_date - last_action_date).days > 1:
                await dao.telegram_user.update_days_active(
                    telegram_id=web_app_init_data.user.id,
                    days_active=1,
                    last_days_active=0,
                )
            elif last_action_date == yesterday_date:
                await dao.telegram_user.update_days_active(
                    telegram_id=web_app_init_data.user.id,
                    days_active=telegram_user.days_active + 1,
                    last_days_active=telegram_user.days_active,
                )
            telegram_user = await dao.telegram_user.update_last_action(
                telegram_id=web_app_init_data.user.id, last_action=datetime.now()
            )
            return telegram_user
