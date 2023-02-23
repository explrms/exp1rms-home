from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
IP = env.str("ip")

HOST = env.str('HOST')
USER = env.str('USER')
PASSWORD = env.str('PASSWORD')
DB = env.str('DB')

YANDEX_TOKEN = env.str('YANDEX_TOKEN')

