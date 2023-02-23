from aiogram import types
from aiogram.dispatcher.filters.builtin import Regexp

from loader import dp
from utils.dicts import device_icons_dict, on_off_icons_dict, on_off_toggle_dict
from utils.iot_api import iot
from utils.logger import logger


class ToggleCallbackData:
    def __init__(self, prefix, action, device_id):
        self.prefix = prefix
        self.action = action
        self.device_id = device_id

    def new(self, **kwargs):
        return ToggleCallbackData(self.prefix, **kwargs)

    def pack(self):
        return f"{self.prefix}:{self.action}:{self.device_id}"

    @staticmethod
    def unpack(data: str):
        prefix, action, device_id = data.split(":")
        return ToggleCallbackData(prefix, action, device_id)


callback_data = ToggleCallbackData("toggle_callback", "action", "device_id")


@dp.callback_query_handler(text='device_list')
async def device_list(call: types.CallbackQuery):
    device_list = await iot.get_device_list()
    rooms = await iot.get_rooms()
    kb = types.InlineKeyboardMarkup()
    for device in device_list:
        on_off = ''
        callback = 'device_list'
        for capability in device['capabilities']:
            if capability['type'] == 'devices.capabilities.on_off':
                on_off = on_off_icons_dict[capability['state']['value']]
                callback = callback_data.new(action=f"toggle_{on_off_toggle_dict[capability['state']['value']]}",
                                  device_id=device['id']).pack()
        kb.add(types.InlineKeyboardButton(text=f'{device_icons_dict[device["type"]]}{on_off} {device["name"]} [{rooms[device["room"]]}]',
                                          callback_data=callback))
    await call.message.edit_text(text='Список устройств:')
    await call.message.edit_reply_markup(kb)


@dp.callback_query_handler(Regexp('toggle_callback'))
async def toggle_callback(call: types.CallbackQuery):
    logger.info(call.data)
    data = callback_data.unpack(call.data)
    logger.info(data)
    match data.action:
        case 'toggle_on':
            code = await iot.toggle_on_device(data.device_id)
        case 'toggle_off':
            code = await iot.toggle_off_device(data.device_id)
        case _:
            code = 404
    if code == 200:
        await device_list(call)
    else:
        await call.answer('Ошибка при выполнении запроса')
