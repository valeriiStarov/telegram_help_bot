import os
from typing import Dict, List, Tuple

import sqlite3
import exceptions


conn = sqlite3.connect('helper_bot.db')
cursor = conn.cursor() 


def insert(table: str, column_values: Dict):
    columns = ', '.join( column_values.keys() )
    values = [tuple(column_values.values())]
    placeholders = ", ".join( "?" * len(column_values.keys()) )
    cursor.executemany(
        f"INSERT INTO {table} "
        f"({columns}) "
        f"VALUES ({placeholders})",
        values)
    conn.commit()


def upp_helper_counter(user_id):
    cursor.execute(
        "SELECT counter FROM helper "
        f"WHERE user_id = '{user_id}'"
    )
    count = cursor.fetchone()
    if count == None:
        raise exceptions.NotCorrectMessage(
            "First you need to use /Can_Help comand"
        )
    count = int(count[0]) + 1

    cursor.execute(
        f"UPDATE helper "
        f"SET counter = '{count}' "
        f"WHERE user_id = '{user_id}' "
    )
    conn.commit()
    return count


def refresh_helper_counter(user_id):
    cursor.execute(
        f"UPDATE helper "
        f"SET counter = 0 "
        f"WHERE user_id = '{user_id}' "
    )
    conn.commit()


def fetchall(table: str, columns: List[str]) -> List[Tuple]:
    columns_joined = ", ".join(columns)
    cursor.execute(f"SELECT {columns_joined} FROM {table}")
    rows = cursor.fetchall()
    result = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result.append(dict_row)
    return result


def delete(table: str, column: str, id: int) -> None:
    id = int(id)
    cursor.execute(f"delete from {table} where {column} = {id}")
    conn.commit()


def get_cursor():
    return cursor


def _init_db():
    """Инициализирует БД"""
    with open("createdb.sql", "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


def check_db_exists():
    """Проверяет, инициализирована ли БД, если нет — инициализирует"""
    cursor.execute("SELECT name FROM sqlite_master "
                   "WHERE type='table' AND name='question'")
    table_exists = cursor.fetchall()
    if table_exists:
        return
    _init_db()

check_db_exists()
