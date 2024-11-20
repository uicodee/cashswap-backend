from aiogram import Dispatcher

from app.tgbot.handlers import commands


def setup(dp: Dispatcher):
    commands.setup(dp)
