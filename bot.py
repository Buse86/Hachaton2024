import asyncio
from operator import index
from pyexpat.errors import messages

import requests
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import *
import requests
import logging
import pandas as pd

# message.from_user.id

users = pd.read_csv('log.csv')
# users = pd.DataFrame(columns=['login', 'password'])

logging.basicConfig(level=logging.INFO)

bot = Bot(token='7897974325:AAE-G0xfOiwGaoNB-5mLoaCsd9pI-dHFrPo')
dp = Dispatcher()

url_login = 'https://test.vcc.uriit.ru/api/auth/login'

headers_login = {'Content-Type': 'application/json'}

# token = requests.post(url_login, headers=headers_login, json=json_login).json()['token']

@dp.message(Command('start'))
async def StartLogin(message: Message):
    await message.answer('Привет! Для продолжения работы нужно авторизоваться')
    await message.answer('Для авторизации напишите /login (логин) (пароль)')
    @dp.message(Command('login'))
    async def asd(message: Message):
        if str(message.from_user.id) not in users.index:
            log = message.text[6:].split()

            json_login = {
                "login": log[0],
                "password": log[1],
                "fingerprint": {}
            }

            ans = requests.post(url_login, headers=headers_login, json=json_login).json()

            try:
                tmp = requests.post(url_login, headers=headers_login, json=json_login).json()['token']
                try:
                    print(users['898461114'])
                    await message.answer(users.index)
                except:
                    pass
                if str(message.from_user.id) not in users.index:
                    users.loc[str(message.from_user.id)] = log
                    users.to_csv('log.csv')
                    print(users)
                await message.answer(f'Вы успешно авторизовались!')
            except:
                await message.answer(ans['detail'] + '\nПопробуйте снова')
        else:
            await message.answer('Вы авторизованы')


async def main():
    await dp.start_polling(bot)

asyncio.run(main())