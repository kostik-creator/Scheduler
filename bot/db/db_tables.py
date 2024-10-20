import os
import psycopg2
from dotenv import load_dotenv

load_dotenv('.env')

# Установка соединения с базой данных PostgreSQL
connection = psycopg2.connect(
    host=os.getenv("host"),
    user=os.getenv("user"),
    password=os.getenv("password"),
    database=os.getenv("db_name"),
    port=os.getenv("port")
)

connection.autocommit = True


def create_tables() -> None:
    """Создать таблицы в базе данных, если они не существуют.

    Эта функция создает две таблицы: `main_users` для хранения информации о пользователях
    и `main_schedule` для хранения напоминаний пользователей.
    """
    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS main_users (
                id serial PRIMARY KEY,
                tg_id integer UNIQUE NOT NULL,
                tg_username varchar(60) UNIQUE
            );"""
        )

    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS main_schedule (
                id serial PRIMARY KEY,
                reminder_text TEXT NOT NULL,
                reminder_datetime TIMESTAMP NOT NULL,
                fk_user_id integer NOT NULL REFERENCES main_users (tg_id) ON DELETE CASCADE
            );"""
        )


create_tables()