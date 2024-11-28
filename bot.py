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
import numpy as np

# message.from_user.id

users = pd.read_csv('log.csv')
# users = pd.DataFrame(columns=['id', 'login', 'password'])

url_vcs = 'https://test.vcc.uriit.ru/api/meetings'
url_login = 'https://test.vcc.uriit.ru/api/auth/login'

logging.basicConfig(level=logging.INFO)

bot = Bot(token='7897974325:AAE-G0xfOiwGaoNB-5mLoaCsd9pI-dHFrPo')
dp = Dispatcher()

headers_login = {'Content-Type': 'application/json'}


# token = requests.post(url_login, headers=headers_login, json=json_login).json()['token']
# @dp.message_handler(commands=['start'])
# async def cmd_start(message: types.Message):
@dp.message(Command('start'))
async def StartLogin(message: Message):
    await message.answer('Привет! Для продолжения работы нужно авторизоваться')
    await message.answer('Для авторизации напишите /login логин пароль')

@dp.message(Command('login'))
async def asd(message: Message):
    if np.int64(message.from_user.id) not in users['id'].values:
        log1 = message.text[6:].split()

        json_login = {
            "login": log1[0],
            "password": log1[1],
            "fingerprint": {}
        }
        log = {'id': str(message.from_user.id), 'login': log1[0], 'password': log1[1]}

        ans = requests.post(url_login, headers=headers_login, json=json_login).json()

        try:
            check = requests.post(url_login, headers=headers_login, json=json_login).json()['token']

            if np.int64(message.from_user.id) not in users['id'].values:
                users.loc[len(users.index)] = log
                users.to_csv('log.csv', index=False)
                print(users)

            await message.answer(f'Вы успешно авторизовались!')

        except:
            await message.answer(ans['detail'] + '\nПопробуйте снова')
    else:
        await message.answer('Вы авторизованы')


@dp.message(Command('vcs'))
async def VCSInfo(message: Message):
    if np.int64(message.from_user.id) in users['id'].values:
        # await message.answer('Введите даты начала и окончания ВКС через пробел, в формате: ГГГГ-ММ-ДД')
        try:
            data = str(message.text)[5:].split()

            jsonlogin = {
                "login": str(users.loc[users['id'].values.tolist().index(message.from_user.id), 'login']),
                "password": str(users.loc[users['id'].values.tolist().index(message.from_user.id), 'password']),
                "fingerprint": {}
            }


            # print(jsonlogin['login'], jsonlogin['password'])

            token = requests.post(url_login, headers=headers_login, json=jsonlogin).json()['token']

            # print(token)


            headers = {
                'Authorization': 'Bearer ' + str(token),
                'Content-Type': 'application/json',
            }


            vcs_ans = []
            info_vcs = ['name', 'startedAt', 'endedAt', 'duration', 'organizedBy']
            for i in ['started', 'ended', 'booked', 'cancelled']:
                params_vcs = {
                    'fromDatetime': f'{data[0]}T00:00:00.000000',
                    'toDatetime': f'{data[1]}T23:59:00.000000',
                    'state': i
                }
                vcs = requests.get(url_vcs, headers=headers, params=params_vcs)
                vcs_ans += vcs.json()['data']
                print(vcs.json()['data'])
            nm = {
                'name': 'Название:',
                "startedAt": 'Начало: ',
                'endedAt': 'Конец',
                'duration': 'Продолжительность',
                'organizedBy': 'Организованно'
            }
            print(vcs_ans)
            for i in vcs_ans:
                await message.answer(i['name'])

        except:
            await message.answer('Вы ввели некорректную дату')

# @dp.message(Command('filter'))
# async def filter(message: Message):
#     await message.answer('1')
#     response = await
#     await message.answer(response)

async def main():
    await dp.start_polling(bot)


asyncio.run(main())