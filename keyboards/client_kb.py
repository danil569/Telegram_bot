from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

kb_client = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/Режим_работы'),
                                                          KeyboardButton('/Расположение'),
                                                          KeyboardButton('/Меню'))

purchase_button = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/Оформить_заказ'),
                                                                KeyboardButton('/Вернуться_в_главное_меню'))
purchase_button1 = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/Оплатить_заказ'),
                                                                 KeyboardButton('/Очистить_корзину'))
purchase_button2 = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Поделиться номером', request_contact=True),
                                                                 KeyboardButton('/К_оплате'))
