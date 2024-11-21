from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.types import WebAppInfo
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from app.config import load_config

router = Router()


@router.message(CommandStart())
async def cmd_start(message: types.Message) -> None:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Join community",
        url="https://t.me/cashcoin_eng"
    )
    builder.button(
        text="Play",
        web_app=WebAppInfo(url="https://miniapp.cashcoin.twc1.net")
    )
    builder.adjust(1)
    await message.answer_photo(
        photo="AgACAgIAAxkBAAMJZz4VxiiYC_RcicJARfjZODa1xGcAAvLtMRv-H_BJsFz47UmqRicBAAMCAAN4AAM2BA",
        caption="🥇 <b>CashCoin</b> is a crypto project with mining and bonuses from other projects. Mine and earn money!\n\n"
                "🌟 <b>CashCoin</b> will do everything for users, and nothing for its own benefit!\n\n"
                "💰 Playing <b>CashCoin</b> will only get more interesting!\n\n",
        reply_markup=builder.as_markup()
    )
