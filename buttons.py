from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton


btn_need_help = KeyboardButton('Need help', callback_data='button1')
btn_can_help = KeyboardButton('Can help', callback_data='button2')
markup_main_menu = ReplyKeyboardMarkup(resize_keyboard=True).row(btn_need_help, btn_can_help)

btn_3 = KeyboardButton('Stop help', callback_data='button3')
btn_4 = KeyboardButton('Go to help', callback_data='button4')
btn_5 = KeyboardButton('Next question', callback_data='button5')
markup_2 = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_4).row(btn_3, btn_5)

btn_6 = KeyboardButton('Delete question', callback_data='button6')
btn_7 = KeyboardButton('Main menu', callback_data='button7')
markup_3 = ReplyKeyboardMarkup(resize_keyboard=True).row(btn_6, btn_7)

markup_4 = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_7)

btn_8 = KeyboardButton('Skip upload screenshot', callback_data='button8')

markup_5 = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_8)


remove_markup = ReplyKeyboardRemove()