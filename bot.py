import asyncio
import requests
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import *
import requests
import logging
import pandas

# message.from_user.id

users = {

}

logging.basicConfig(level=logging.INFO)

bot = Bot(token='7897974325:AAE-G0xfOiwGaoNB-5mLoaCsd9pI-dHFrPo')
dp = Dispatcher()

url_login = 'https://test.vcc.uriit.ru/api/auth/login'

headers_login = {'Content-Type': 'application/json'}

# token = requests.post(url_login, headers=headers_login, json=json_login).json()['token']

@dp.message(Command('start'))
async def echo(message: Message):
    # kb = [[types.KeyboardButton(text="Авторизироваться")]]
    # keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await message.answer('Привет! Для продолжения работы нужно авторизоваться')
    await message.answer('Для авторизации напишите /login (логин) (пароль)')


@dp.message(Command('login'))
async def asd(message: Message):
    log = message.text[6:].split()

    json_login = {
        "login": log[0],
        "password": log[1],
        "fingerprint": {}
    }

    ans = requests.post(url_login, headers=headers_login, json=json_login).json()

    try:
        tmp = ans['token']
        await message.answer(f'Вы успешно авторизовались! {log[0]} {log[1]}')
        if str(message.from_user.id) not in users:
            users[str(message.from_user.id)] = log
    except:
        await message.answer(ans['detail'])

async def main():
    await dp.start_polling(bot)

asyncio.run(main())