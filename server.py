import os

from aiogram import Bot, Dispatcher, executor, types

import db_logic
from buttons import *
import db
import exceptions

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.


API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

def get_dp():
    return dp

class Form(StatesGroup):
    question = State()


@dp.message_handler(text = 'Main menu')
@dp.message_handler(text = 'Skip upload screenshot')
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.answer(
        'This bot connecting people\n'
        '/Need_Help - Ask your question and bot help you to find person who can help you.\n'
        '/Can_Help - You can help other people find answers of they questions.', reply_markup=markup_main_menu)
    

@dp.message_handler(text='Need help')
@dp.message_handler(commands=['Need_Help'])
async def need_help(message: types.Message):

    question = db_logic.check_question_exist(message.chat.id)
    if question:
        answer_message = (
            f'{question[1]}'
            '\n------------------------------------\n'
            'You already have active question\n'
            'If you want to write new question, you need to delete active question\n'
            # question[1] - текст вопроса
        )
        markup = markup_3

        try:
            await db_logic.get_photo(
                                    message.chat.id,
                                    question[0],
                                    answer_message,
                                    markup
                                    )
            
        except exceptions.DoesNotExistPhotoPath:
            await message.answer(answer_message, reply_markup=markup)

    else:
        await Form.question.set()
        answer_message = (
            'Here you can describe your problem.\n'
        'Please indicate your OS and technology with which your question is related, so that the helpers can help you faster.\n'
        'For example: MacOS / Django'
        )
        markup = markup_4
        await message.answer(answer_message, reply_markup=markup,)


@dp.message_handler(state=Form.question)
async def take_question(message: types.Message, state: FSMContext):
    try:
        question = db_logic.add_question(message)
        answer_message = (
            'Bot add your question:'
            '\n---------------------------------------\n'
            f'{question}'
            '\n---------------------------------------\n'
            'Optional, here you can upload screenshot of your question\n'
            "That's speed up finding the answer of question"
            )
        markup = markup_5
    except Exception as e:
        answer_message = (f'{e}')
        markup = markup_main_menu
    await message.answer(answer_message, reply_markup=markup)
    await state.finish()


@dp.message_handler(content_types=types.ContentType.PHOTO)
async def take_photo(message: types.Message, state: FSMContext):
    path = f'./media/{message.chat.id}.jpg'
    await message.photo[-1].download(destination_file=path)
    answer_message = (
        'Successful upload your screenshot! Thanks for screenshot!'
    )
    markup = markup_main_menu
    await message.answer(answer_message, reply_markup=markup)


@dp.message_handler(text='Delete question')
@dp.message_handler(commands=['Delete_Question'])
async def delete_question(message: types.Message):
    db_logic.delete_question(message.chat.id)
    db_logic.delete_photo(message.chat.id)
    await message.answer('your question has been deleted',reply_markup=markup_main_menu)


@dp.message_handler(text='Can help')
@dp.message_handler(commands=['Can_Help'])
async def can_help(message: types.Message):
    helper = db_logic.add_helper(message.chat.id, 0)

    try:
        number = db.upp_helper_counter(message.chat.id)

        question = db_logic.choose_one_question(number)
        #choose_one_question[1] - Текст вопроса
        answer_message = (
        f'Question # {int(number)}:\n{question[1]}'
        )
        markup = markup_2

        try:
            await db_logic.get_photo(
                                    message.chat.id,
                                    question[0],
                                    answer_message,
                                    markup
                                    )
            
        except exceptions.DoesNotExistPhotoPath:
            await message.answer(answer_message, reply_markup=markup)


    except exceptions.NoQuestions as e:
        answer_message = (f'{e}')
        markup = markup_main_menu
        await message.answer(answer_message, reply_markup=markup)
    

@dp.message_handler(text='Next question')
@dp.message_handler(commands=['Next_Question'])
async def next_question(message: types.Message):
    try:
        number = db.upp_helper_counter(message.chat.id)
        question = db_logic.choose_one_question(number)
        #choose_one_question[1] - Текст вопроса
        answer_message = (
        f'Question # {int(number)}:\n{question[1]}'
        )
        markup = markup_2

        if await db_logic.get_photo(
                                    message.chat.id,
                                    question[0],
                                    answer_message,
                                    markup
                                   ):
            return True
        else:
            await message.answer(answer_message, reply_markup=markup) 
        

    except (exceptions.NotCorrectMessage, exceptions.OutOfQuestions) as e:
        answer_message = (f'{e}')
        markup = markup_main_menu
        await message.answer(answer_message, reply_markup=markup)


@dp.message_handler(text='Go to help')
@dp.message_handler(commands=['Go_To_Help'])
async def go_to_help(message: types.Message):
    try:
        number = db_logic.choose_number_of_question(message.chat.id)
        question = db_logic.choose_one_question(number)
        #choose_one_question[1] - Текст вопроса
        #choose_one_question[2] - user_id автора вопроса
        answer_message = (
        f'Question # {int(number)}:\n{question[1]}\n\n'
        f'<a href="tg://user?id={question[0]}">Author</a> of question'
        )
        
        markup = markup_2

    except exceptions.NotCorrectMessage as e:
        answer_message = (f'{e}')
        markup = markup_main_menu
    except exceptions.OutOfQuestions as e:
        answer_message = (f'{e}')
        markup = markup_main_menu

    await message.answer(answer_message, reply_markup=markup, parse_mode='HTML')


@dp.message_handler(text='Stop help')
@dp.message_handler(commands=['Stop_Help'])
async def stop_help(message: types.Message):
    db_logic.delete_helper(message.chat.id)
    db.refresh_helper_counter(message.chat.id)
    await message.answer('Thank you for your attention! Good luck!', reply_markup=markup_main_menu)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)