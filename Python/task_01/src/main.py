import psycopg2
import logging
import requests
from datetime import datetime, timedelta
import cfg


class CurrencyDataHandler:
    def __init__(self, api_key, dbname, user, password, host, port):
        logging.basicConfig(filename="../logs/error.log", level=logging.ERROR)

        self.api_key = api_key

        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

        self.conn = None
        self.cursor = None

    def connect_to_database(self):
        try:
            print
            self.conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
            )
            self.cursor = self.conn.cursor()
            print("Успешное подключение к базе данных PostgreSQL!")
        except psycopg2.Error as e:
            logging.error(f"Ошибка при подключении к базе данных PostgreSQL: {e}")

    def close_connection(self):
        if self.conn is not None:
            self.conn.close()
            print("Соединение с базой данных закрыто.")

    def insert_data(self, data_to_insert):
        if self.cursor is not None:
            insert_query = "INSERT INTO rates (usd, eur) VALUES (%s, %s)"
            self.cursor.execute(insert_query, data_to_insert)
            self.conn.commit()
            print("Данные успешно добавлены в базу данных.")

    @staticmethod
    def get_yesterday_date():
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        return yesterday

    @staticmethod
    def get_json_data(url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            logging.error(
                f"Не удалось получить данные. Код ответа: {response.status_code}"
            )
            return

    def check_today_insert(self):
        select_date = (
            "SELECT * FROM rates WHERE DATE(insert_date)="
            + "'"
            + str(datetime.now().date())
            + "'"
        )
        self.cursor.execute(select_date)

        return self.cursor.fetchall()

    def process_currency_data(self):
        if len(self.check_today_insert()) == 0:
            return

        yesterday_date = self.get_yesterday_date()
        # Base не работает в бесплатном плане
        url = (
            f"http://data.fixer.io/api/{yesterday_date}?access_key="
            + self.api_key
            + "&symbols=USD,EUR"
        )
        json_data = self.get_json_data(url)

        if json_data["success"] == True:
            usd_rate = json_data["rates"]["USD"]
            eur_rate = json_data["rates"]["EUR"]

            print(f"Курс USD на вчерашнюю дату: {usd_rate}")
            print(f"Курс EUR на вчерашнюю дату: {eur_rate}")

            data_to_insert = (usd_rate, eur_rate)
            self.insert_data(data_to_insert)
        else:
            logging.error(f"API ошибка: {json_data}")


if __name__ == "__main__":
    handler = CurrencyDataHandler(
        api_key=cfg.api_key,
        dbname=cfg.dbname,
        user=cfg.user,
        password=cfg.password,
        host=cfg.host,
        port=cfg.port,
    )

    handler.connect_to_database()
    handler.process_currency_data()
    handler.close_connection()
