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

    async def load_color_code_by_name(self, color: str) -> str:
        """
        Бутафорская функция. Нужна для примера взаимодействия экземпляра класса IOT с базой данных
        :param color:
        :return: color_code: str

        Example:
        >>> await db.load_color_code_by_name('red')
        >>> '#FF0000'
        """
        with self.__base.cursor() as curs:
            curs.execute('SELECT color_code '
                         'FROM color_setups '
                         'WHERE color_name = %s', (
                             color
                         ))
            color_code = curs.fetchone()[0]
            return color_code


db = SQL()
