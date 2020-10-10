import psycopg2
from psycopg2 import sql
from psycopg2.extras import DictCursor
import configparser
import os

DIR_NAME = os.path.dirname(os.path.abspath(__file__))


class SQLInjection:
    """
    Базовый класс для работы с базой данных
    """
    def __init__(self):
        """
        Инициализация подключения к БД
        """
        config = configparser.ConfigParser()
        config.read(DIR_NAME + "/settings.ini")

        try:
            self.con = psycopg2.connect(
                dbname=config["BD"]["dbname"],
                user=config["BD"]["user"],
                password=config["BD"]["password"],
                host=config["BD"]["host"],
                port=config["BD"]["port"]
            )
        except psycopg2.DatabaseError as e:
            print("ERROR: {}".format(e))

    def __call__(self, sqlcommand, **kwargs):
        """
        Выополнение sql скрипта
        :param sqlcommand: текст sql
        :param kwargs: динамические параметры
        :return: ответ от БД
        """
        with self.con.cursor(cursor_factory=DictCursor) as cursor:
            try:
                com = sql.SQL(sqlcommand).format(kwargs)
                cursor.execute(com)
                try:
                    result = cursor.fetchall()
                    self.con.commit()
                    return result
                except:
                    self.con.commit()
            except psycopg2.DatabaseError as e:
                print('DBError: {}'.format(e))
                self.con.rollback()
