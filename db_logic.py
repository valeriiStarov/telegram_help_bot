
from typing import List, NamedTuple, Optional
from aiogram.types import InputFile
import os
import db
import exceptions
import buttons
from server import get_dp


class Question(NamedTuple):
    """Структура добавленного в БД нового вопроса"""
    id: Optional[int]
    text: str
    user_id: int


class Helper(NamedTuple):
    """Структура добавления в БД нового помощника"""
    user_id: int
    counter: int


class RandomQuestion(NamedTuple):
    """Структура случайного вопроса для helper'a"""
    text: str


def add_question(message) -> Question:
    """Добавляет новое сообщение.
    Принимает на вход текст сообщения, пришедшего в бот."""

    text = str(message.text)
    if text[0] == '/':
        raise exceptions.NotCorrectMessage(
            "Question can't start with '/'\n"
            "Try starting with a different character."
            )
    if text == buttons.btn_7.text:
        raise exceptions.MainMenuQuestion(
            'You returned in main menu\n'
        )

    insert_question = db.insert('question', {
        'text': str(message.text),
        'user_id': int(message.chat.id)
    })
    return text


def choose_number_of_question(user_id):
    """Возвращает последний вопрос"""
    cursor = db.get_cursor()
    cursor.execute(
        "SELECT counter FROM helper "
        f"WHERE user_id = '{user_id}'"
    )
    count = cursor.fetchone()
    if count == None:
        raise exceptions.NotCorrectMessage(
            "First you need to use /Can_Help comand"
        )
    return int(count[0])


def choose_one_question(number) -> str:
    """Возвращает все вопросы в виде списка"""

    cursor = db.get_cursor()
    cursor.execute(
        "SELECT * FROM question"
    )
    count = cursor.fetchall()
    if count == []:
        raise exceptions.NoQuestions(
            "Sorry we don't have any questions for you.\n"
            "So far no one needs help :("
        )
    result = []
    for c in count:
        result.insert(0, c)
    try:
        result[number-1]
    except IndexError:
        raise exceptions.OutOfQuestions(
            f"You have viewed all {number-1} questions! You awesome!\n"
            "You can watch them again, if you want change your choice.\n"
            "For that you need to run - /Can_Help\n"
            "Good luck!\n"
        )

    return result[number-1]


def check_question_exist(user_id) -> Question:
    """Проверяет есть ли у пользователя вопрос и возвращает его если есть"""
    cursor = db.get_cursor()
    cursor.execute(
        "SELECT * FROM question "
        f"WHERE user_id = '{user_id}'"
    )
    question = cursor.fetchone()
    if question:
        return question
    else:
        return False


def delete_question(user_id) -> None:
    """Удаляет вопрос"""
    db.delete('question', 'user_id', user_id)


def check_helper_exist(user_id) -> bool:
    """Проверяет есть ли уже в БД данный пользователь"""
    cursor = db.get_cursor()
    cursor.execute(
        "SELECT user_id FROM helper "
        f"WHERE user_id = '{user_id}'"
    )
    if cursor.fetchone():
        db.refresh_helper_counter(user_id=user_id)
        return True
    return False


def add_helper(user_id, counter) -> Helper:
    """Добавляет нового помощника в БД"""
    
    if check_helper_exist(user_id):
        return Helper(user_id=user_id, counter=counter)

    insert_helper = db.insert('helper', {
        'user_id': int(user_id),
        'counter': counter
    })
    return Helper(user_id=user_id, counter=counter)


def get_photo(chat_id, user_id, caption, markup):
    # user_id - id автора вопроса
    path = f'./media/{user_id}.jpg'
    dp = get_dp()
    try: 
        return (dp.bot.send_photo(
            chat_id=chat_id,
            photo = InputFile(path_or_bytesio=path),
            caption=caption,
            reply_markup=markup
            ))

    except FileNotFoundError:
        raise exceptions.DoesNotExistPhotoPath()


def delete_photo(user_id) -> None:
    path = f'./media/{user_id}.jpg'
    try:
        return os.remove(path)
    except FileNotFoundError:
        False


def delete_helper(user_id) -> None:
    """Удаляет helper'a по его идентификатору"""
    db.delete('helper', 'user_id', user_id)

def delete_question(user_id) -> None:
    """Удаляет вопрос"""
    db.delete('question', 'user_id', user_id)