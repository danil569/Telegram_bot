from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import bot, dp
from keyboards.client_kb import kb_client, purchase_button, purchase_button1, purchase_button2
from data_base import sqlite_db
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

basket = []


class FSMClient(StatesGroup):
    order = State()
    price = State()


# @dp.message_handler(commands=['start', 'help', 'Вернуться_в_главное_меню'])
async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Добро пожаловать', reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply('Пожалуйста, напишите боту в ЛС:\nhttps://t.me/madinachaihonabot')


# @dp.message_handler(commands=['Режим_работы'])
async def command_working_hours(message: types.Message):
    await bot.send_message(message.from_user.id, 'Мы работаем каждый день с 11:00 до 24:00')


# @dp.message_handler(commands=['Расположение'])
async def command_place(message: types.Message):
    await bot.send_message(message.from_user.id, 'Мы находимся по адресу: ул. XXXXX, строение 1')


# @dp.message_handler(commands=['Меню'])
async def command_menu(message: types.Message):
    read = await sqlite_db.sql_read()
    for ret in read:
        await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена {ret[-1]} руб.', reply_markup=purchase_button)
        await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup().\
                               add(InlineKeyboardButton(f'Добавить в корзину', callback_data=f'add {ret[1]} {ret[-1]}')))


# @dp.message_handler(commands=['Оформить_заказ'])
async def command_order(message: types.Message):
    order_price = sum(float(i.split()[1]) for i in basket)
    order = "\n".join(i for i in basket)
    await bot.send_message(message.from_user.id, text=f'Ваш заказ:\n{order}\n Сумма заказа {order_price} рублей.\n'
                                                      f'Пожалуйста, отправьте номер для подтверждения заказа',
                           reply_markup=purchase_button2)


# @dp.message_handler(commands=['Очистить_корзину'])
async def command_change(message: types.Message):
    global basket
    basket = []
    await bot.send_message(message.from_user.id, text='Корзина очищена',
                           reply_markup=kb_client)


# @dp.callback_query_handler(lambda x: x.data and x.data.startswith('basket_del '))
async def del_from_basket_callback_run(callback_query: types.CallbackQuery):
    item_to_basket = callback_query.data.replace('basket_del ', '')
    global basket
    del basket[basket.index(item_to_basket)]
    await callback_query.answer(text=f'{callback_query.data.replace("basket_del ", "")} удален из корзины.', show_alert=True)


# @dp.message_handler(commands=['Оплатить_заказ', 'К_оплате'])
async def command_pay(message: types.Message):
    await bot.send_message(message.from_user.id, text='Оплатите по ссылке ниже:', reply_markup=InlineKeyboardMarkup().\
                           add(InlineKeyboardButton(text='Оплатить QIWI', url='https://qiwi.com/payment')))


# @dp.callback_query_handler(lambda x: x.data and x.data.startswith('add '))
async def add_to_basket_callback_run(callback_query: types.CallbackQuery):
    item_to_basket = callback_query.data.replace('add ', '')
    global basket
    basket.append(item_to_basket)
    await callback_query.answer(text=f'{callback_query.data.replace("add ", "")} добавлен в корзину.', show_alert=True)


# @dp.message_handler(content_types=['contact'])
async def command_contact(message):
    if message.contact is not None:
        await bot.send_message(message.from_user.id, text='Вы успешно отправили номер', reply_markup=purchase_button1)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help', 'Вернуться_в_главное_меню'])
    dp.register_message_handler(command_working_hours, commands=['Режим_работы'])
    dp.register_message_handler(command_place, commands=['Расположение'])
    dp.register_message_handler(command_menu, commands=['Меню'])
    dp.register_message_handler(command_pay, commands=['Оплатить_заказ', 'К_оплате'])
    dp.register_message_handler(command_order, commands=['Оформить_заказ'])
    dp.register_message_handler(command_change, commands=['Очистить_корзину'])
    dp.register_message_handler(command_contact, content_types=['contact'])
    dp.register_callback_query_handler(add_to_basket_callback_run, lambda x: x.data and x.data.startswith('add '))
    dp.register_callback_query_handler(del_from_basket_callback_run, lambda x: x.data and x.data.startswith('basket_del '))
