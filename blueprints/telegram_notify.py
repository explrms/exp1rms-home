from quart import Blueprint, request

from data.config import ADMINS
from loader import dp

telegram_notify = Blueprint('telegram_notify', __name__)


@telegram_notify.route('/')
async def index():
    text = request.args.get('text')
    await dp.bot.send_message(chat_id=ADMINS[0], text=text)
    return {'response': {'status': 'ok'}}
