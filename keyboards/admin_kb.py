from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data_base import sqlite_db


inline_callback = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Загрузить', callback_data='загрузить'),\
                                                        InlineKeyboardButton(text='Удалить', callback_data='удалить'))

but_load = KeyboardButton('/Загрузить')
but_del = KeyboardButton('/Удалить')

kb_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/Загрузить'),
                                                         KeyboardButton('/Удалить'))

