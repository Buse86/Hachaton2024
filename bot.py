import asyncio
import requests
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import *
import requests

users = {
    'id2': ['login', 'password'],
}

bot = Bot(token='6908813524:AAEwHxUdwjGZO_q_eb9UZszRkVxjZXU4k8k')
dp = Dispatcher()

url_login = 'https://test.vcc.uriit.ru/api/auth/login'

json_login = {
  "login": "hantaton082",
  "password": "apyNbPS5Wr8^PbCg",
  "fingerprint": {}
}

headers_login = {'Content-Type': 'application/json'}

# token = requests.post(url_login, headers=headers_login, json=json_login).json()['token']

@dp.message(CommandStart())
async def echo(message: Message):
    await message.answer('Приветствую!')
    await message.answer('Как тебя зовут?')

@dp.message(F.text)
async def asd(message: Message):
    qwezxc = requests.post(url_login, headers=headers_login, json=json_login).json()
    kb = [[types.KeyboardButton(text="Авторизироваться")],
    ]

    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    #await message.answer("Приветствую!", reply_markup=keyboard)

    try:
        qwe666 = qwezxc['token']
        await message.answer(qwe666)
    except:
        await message.answer('ты красотка')

async def main():
    await dp.start_polling(bot)

asyncio.run(main())