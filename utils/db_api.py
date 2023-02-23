import logging

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from data import config


class SQL:

    def __init__(self) -> None:
        try:
            self.__base = psycopg2.connect(
                host=config.HOST,
                user=config.USER,
                password=config.PASSWORD,
                database=config.DB,
            )
            self.__base.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            self.__base.autocommit = True
            print('Database %s: connection is successful' % config.DB)
        except Exception as ex:
            logging.exception('Something went wrong while connecting to db - %s' % ex)

    async def check_access(self, tg_id: int) -> bool:
        """
        Проверка, есть ли доступ к боту к конкретного пользователя
        :param tg_id:
        :return: bool
        """
        with self.__base.cursor() as curs:
            curs.execute('SELECT access FROM users WHERE tg_id = %s', (tg_id,))
            result = curs.fetchone()
        return result[0]


db = SQL()
