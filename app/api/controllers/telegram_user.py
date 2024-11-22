from datetime import timedelta, datetime, timezone

from fastapi import APIRouter, Depends, Path, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import PositiveInt

from app import dto
from app.api import schems
from app.api.dependencies import get_telegram_user, dao_provider
from app.infrastructure.database import HolderDao

router = APIRouter(prefix="/telegram-user")
moscow_tz = timezone(timedelta(hours=3))


@router.get(
    path="/", response_model=list[dto.TelegramUser], description="Get telegram users"
)
async def get_all(dao: HolderDao = Depends(dao_provider)) -> list[dto.TelegramUser]:
    return await dao.telegram_user.get_all()


@router.get(
    path="/referrals",
    response_model=list[dto.TelegramUser],
    description="Get telegram user referrals",
)
async def get_all_referrals(
        telegram_user: dto.TelegramUser = Depends(get_telegram_user),
        dao: HolderDao = Depends(dao_provider),
) -> list[dto.TelegramUser]:
    return await dao.telegram_user.get_all_referrals(
        telegram_id=telegram_user.telegram_id
    )


@router.get(
    path="/referrals/{telegram_id}",
    response_model=list[dto.TelegramUser],
    description="Get telegram user referrals",
)
async def get_all_referrals_by_id(
        telegram_id: PositiveInt = Path(), dao: HolderDao = Depends(dao_provider)
) -> list[dto.TelegramUser]:
    return await dao.telegram_user.get_all_referrals(telegram_id=telegram_id)


@router.put(
    path="/{telegram_id}",
    response_model=dto.TelegramUser,
    description="Update telegram user",
)
async def update_telegram_user(
        telegram_user: schems.UpdateTelegramUser,
        telegram_id: PositiveInt = Path(),
        dao: HolderDao = Depends(dao_provider),
) -> dto.TelegramUser:
    return await dao.telegram_user.update_one(
        telegram_id=telegram_id, telegram_user=telegram_user
    )


@router.post(path="/claim-daily", response_model=dto.TelegramUser, description="Claim")
async def claim_daily_earning(
        telegram_user: dto.TelegramUser = Depends(get_telegram_user),
        dao: HolderDao = Depends(dao_provider),
) -> dto.TelegramUser:
    current_time = datetime.now(moscow_tz)
    if telegram_user.last_daily_reward:
        if telegram_user.last_daily_reward.date() == current_time.date():
            raise HTTPException(
                status_code=400, detail="Daily reward already claimed today"
            )
    await dao.telegram_user.update_last_daily_reward(
        telegram_id=telegram_user.telegram_id, last_daily_reward=current_time
    )
    await dao.telegram_user.update_user_balance(
        telegram_id=telegram_user.telegram_id, balance=telegram_user.balance + telegram_user.days_active * 50
    )
    updated_user = await dao.telegram_user.update_user_tickets(
        telegram_id=telegram_user.telegram_id,
        tickets=telegram_user.tickets + telegram_user.days_active * 1 if telegram_user.days_active < 5 else 5,
    )
    return updated_user


@router.post(path="/claim", response_model=dto.TelegramUser, description="Claim")
async def claim_earning(
        telegram_user: dto.TelegramUser = Depends(get_telegram_user),
        dao: HolderDao = Depends(dao_provider),
) -> dto.TelegramUser:
    current_time = datetime.now(moscow_tz)
    if current_time <= telegram_user.next_farm.astimezone(moscow_tz):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="It's not time to claim"
        )
    current_user = await dao.telegram_user.update_balance(
        telegram_id=telegram_user.telegram_id,
        balance=telegram_user.balance + 100,
        last_farm=current_time,
        next_farm=current_time + timedelta(hours=8),
    )
    if telegram_user.referrer_id is not None:
        referrer = await dao.telegram_user.get_telegram_user(
            telegram_id=telegram_user.referrer_id
        )
        await dao.telegram_user.update_user_extra_balance(
            telegram_id=telegram_user.referrer_id,
            extra_balance=referrer.extra_balance + 10,
        )
        if referrer.referrer_id is not None:
            referrer_referrer = await dao.telegram_user.get_telegram_user(
                telegram_id=referrer.referrer_id
            )
            await dao.telegram_user.update_user_extra_balance(
                telegram_id=referrer.referrer_id,
                extra_balance=referrer_referrer.extra_balance + 2.5,
            )
    return current_user


@router.post(path="/claim-extra", response_model=dto.TelegramUser, description="Claim")
async def claim_extra_earning(
        telegram_user: dto.TelegramUser = Depends(get_telegram_user),
        dao: HolderDao = Depends(dao_provider),
) -> dto.TelegramUser:
    if telegram_user.extra_balance > 0:
        await dao.telegram_user.update_user_balance(
            telegram_id=telegram_user.telegram_id,
            balance=telegram_user.balance + telegram_user.extra_balance
        )
        await dao.telegram_user.update_user_extra_balance(
            telegram_id=telegram_user.telegram_id,
            extra_balance=0
        )
        return telegram_user
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No extra balance"
        )


@router.get(path="/get-me", response_model=dto.TelegramUser, description="Get me")
async def get_me(
        telegram_user: dto.TelegramUser = Depends(get_telegram_user),
) -> dto.TelegramUser:
    max_farm_per_hour = 100 / 8

    last_farm = telegram_user.last_farm.astimezone(moscow_tz)
    next_farm = telegram_user.next_farm.astimezone(moscow_tz)
    current_time = datetime.now(moscow_tz)

    if current_time >= next_farm:
        telegram_user.already_farmed = 100
        telegram_user.percent = 100
        return telegram_user

    if (current_time - last_farm).total_seconds() < 60:
        telegram_user.already_farmed = 0
        telegram_user.percent = 0
        return telegram_user

    hours_passed = (current_time - last_farm).total_seconds() / 3600

    already_farmed = min(hours_passed * max_farm_per_hour, 100)
    telegram_user.already_farmed = round(already_farmed, 2)

    telegram_user.percent = int(round((telegram_user.already_farmed / 100) * 100, 2))
    return telegram_user


@router.get(path="/rating", response_model=dto.Rating, description="Get rating")
async def get_rating(
        telegram_user: dto.TelegramUser = Depends(get_telegram_user),
        dao: HolderDao = Depends(dao_provider),
) -> dto.Rating:
    place = await dao.telegram_user.get_user_rank(telegram_id=telegram_user.telegram_id)
    return dto.Rating(place=place)


@router.get(
    path="/leaderboard",
    response_model=list[dto.TelegramUser],
    description="Get leaderboard",
)
async def get_leaderboard(
        dao: HolderDao = Depends(dao_provider),
) -> list[dto.TelegramUser]:
    return await dao.telegram_user.get_users_by_rank()
