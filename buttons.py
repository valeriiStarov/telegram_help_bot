from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton


btn_need_help = KeyboardButton('Need help', callback_data='button1')
btn_can_help = KeyboardButton('Can help', callback_data='button2')
markup_main_menu = ReplyKeyboardMarkup(resize_keyboard=True).row(btn_need_help, btn_can_help)

btn_stop_help = KeyboardButton('Stop help', callback_data='button3')
btn_go_to_help = KeyboardButton('Go to help', callback_data='button4')
btn_next_question = KeyboardButton('Next question', callback_data='button5')
markup_help_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_go_to_help).row(btn_stop_help, btn_next_question)

btn_delete_question = KeyboardButton('Delete question', callback_data='button6')
btn_main_menu = KeyboardButton('Main menu', callback_data='button7')
markup_if_have_question_menu = ReplyKeyboardMarkup(resize_keyboard=True).row(btn_delete_question, btn_main_menu)

markup_if_no_question_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_main_menu)

btn_skip_upload_photo = KeyboardButton('Skip upload screenshot', callback_data='button8')

markup_skip_upload_photo = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_skip_upload_photo)


remove_markup = ReplyKeyboardRemove()