from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from utils.db_api import db


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    if db.check_access(message.from_user.id):
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(text='📃Список устройств', callback_data='device_list'))
        await message.answer(f"Добро пожаловать, {message.from_user.first_name}",
                             reply_markup=kb)
    else:
        await message.answer('У вас нет доступа к этому боту')
