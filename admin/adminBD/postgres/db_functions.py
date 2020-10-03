import psycopg2
import configparser


class SQLInjection(object):
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("settings.ini")

        try:
            self.con = psycopg2.connect(
                dbname=config["BD"]["dbname"],
                user=config["BD"]["user"],
                password=config["BD"]["password"],
                host=config["BD"]["host"],
                port=config["BD"]["port"]
            )
            print("Connection successful")
        except psycopg2.DatabaseError as e:
            print("ERROR: {}".format(e))

    def __call__(self, sqlcommand, **kwargs):
        with self.con.cursor() as cursor:
            try:
                cursor.execute(sqlcommand)
                cursor.commit()
            except psycopg2.DatabaseError as e:
                cursor.rollback()
                print('DBError: '.format(e))
