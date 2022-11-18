"""Кастомные исключения, генерируемые приложением"""


class NotCorrectMessage(Exception):
    """Некорректное сообщение в бот, которое не удалось распарсить"""
    pass


class OutOfQuestions(Exception):
    """Используется как маркер окончания списка вопросов"""
    pass

class NoQuestions(Exception):
    """Список вопросов пуст"""
    pass

class MainMenuQuestion(Exception):
    """Исключает команду Main menu"""
    pass

class DoesNotExistPhotoPath(Exception):
    """У данного пользователя нет фото"""