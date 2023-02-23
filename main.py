from multiprocessing import Process

from quart import Quart

from blueprints.telegram_notify import telegram_notify
from bot import bot_starter

app = Quart(__name__)
app.register_blueprint(telegram_notify, url_prefix="/telegram_notify")


if __name__ == '__main__':
    bot_process = Process(target=bot_starter, daemon=True)
    bot_process.start()
    app.run(host='141.8.199.234', port=80)
