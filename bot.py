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
# users = pd.DataFrame(columns=['id', 'login', 'password', 'create', 'VCScreate', 'filter'])

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

        log = {'id': str(message.from_user.id), 'login': log1[0], 'password': log1[1], 'create': 0, 'VCScreate': '', 'filter': ''}

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
        await message.answer('Введите даты начала и окончания ВКС через пробел, в формате: ГГГГ-ММ-ДД')
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
                # org = requests.get('https://test.vcc.uriit.ru/api/catalogs/departments/' + i['organizedBy'], headers=headers, params={'department_id': i['organizedBy']}).json()['name']
                await message.answer(f'''Название: {i['name']}
Дата начала: {i['startedAt']}
Дата окончания: {i['endedAt']}
Продолжительность: {i['duration']} минут
''')

        except:
            await message.answer('Вы ввели некорректную дату')

# @dp.message(Command('filter'))
# async def filter(message: Message):
#     await message.answer('1')
#     response = await
#     await message.answer(response)


    # await message.answer('Чтобы создать новую ВКС, введите её название:')
    # response = await dp.wait_for_message(chat_id=message.chat.id)
    # vcs_info['Название'] = response.text
    #
    # await message.answer('Выберите место проведения:')
    # response = await dp.wait_for_message(chat_id=message.chat.id)
    # vcs_info['Место'] = response.text
    #
    # await message.answer('Выберите помещение:')
    # response = await dp.wait_for_message(chat_id=message.chat.id)
    # vcs_info['Помещение'] = response.text
    #
    # await message.answer('Введите дату и время начала ВКС (в формате ГГГГ-ММ-ДД ЧЧ:ММ:СС):')
    # response = await dp.wait_for_message(chat_id=message.chat.id)
    # vcs_info['Дата и время начала'] = response.text
    #
    # await message.answer('Введите продолжительность ВКС (в формате ЧЧ:ММ:СС):')
    # response = await dp.wait_for_message(chat_id=message.chat.id)
    # vcs_info['Продолжительность'] = response.text
    #
    # await message.answer('Введите участников ВКС, в формате e-mail:')
    # response = await dp.wait_for_message(chat_id=message.chat.id)
    # vcs_info['Участники'] = response.text
    #
    # await message.answer('Введите максимальное количество участников ВКС:')
    # response = await dp.wait_for_message(chat_id=message.chat.id)
    # vcs_info['Максимальное количество участников'] = response.text
    #
    # await message.answer('Введите средство проведения ВКС:')
    # response = await dp.wait_for_message(chat_id=message.chat.id)
    # vcs_info['Средство проведения'] = response.text

@dp.message(Command('create'))
async def CreateVcs(message: Message):
    users.loc[users['id'].values.tolist().index(message.from_user.id), 'сreate'] = 1
    await message.answer('Чтобы создать новую ВКС, введите название ВКС')

@dp.message(Command('cancel'))
async def CanсelVcs(message: Message):
    users.loc[users['id'].values.tolist().index(message.from_user.id), 'сreate'] = 0
    users.loc[users['id'].values.tolist().index(message.from_user.id), 'VCScreate'] = ''
    await message.answer('Cоздание ВКС отменено')

@dp.message()
async def CreateVcs1(message: Message):
    if users.loc[users['id'].values.tolist().index(message.from_user.id), 'сreate'] == 1:
        users.loc[users['id'].values.tolist().index(message.from_user.id), 'сreate'] = 2
        response = message.text
        users.loc[users['id'].values.tolist().index(message.from_user.id), 'VCScreate'] = response
        users.to_csv('log.csv', index=False)
        await message.answer('Введите время начала конференции (гггг-мм-дд чч:мм)')

    elif users.loc[users['id'].values.tolist().index(message.from_user.id), 'сreate'] == 2:
        users.loc[users['id'].values.tolist().index(message.from_user.id), 'сreate'] = 3

        response = message.text
        tmp = response.split()[1]
        response = response.replace(' ', f'T{tmp}:00.000000')[:-5]

        users.loc[users['id'].values.tolist().index(message.from_user.id), 'VCScreate'] = users.loc[users['id'].values.tolist().index(message.from_user.id), 'VCScreate'] + ';' + str(response)
        users.to_csv('log.csv', index=False)
        await message.answer('Введите максимальное кол-во участников конференции')

    elif users.loc[users['id'].values.tolist().index(message.from_user.id), 'сreate'] == 3:
        users.loc[users['id'].values.tolist().index(message.from_user.id), 'сreate'] = 4

        response = message.text
        users.loc[users['id'].values.tolist().index(message.from_user.id), 'VCScreate'] += ';' + response
        users.to_csv('log.csv', index=False)
        await message.answer('Введите продoлжительность конференции в минутах')

    elif users.loc[users['id'].values.tolist().index(message.from_user.id), 'сreate'] == 4:
        users.loc[users['id'].values.tolist().index(message.from_user.id), 'сreate'] = 5
        response = message.text
        users.loc[users['id'].values.tolist().index(message.from_user.id), 'VCScreate'] += ';' + response
        users.to_csv('log.csv', index=False)
        await message.answer('''Введите ( . ) ( . )
           .!.''')

    elif users.loc[users['id'].values.tolist().index(message.from_user.id), 'сreate'] == 5:
        users.loc[users['id'].values.tolist().index(message.from_user.id), 'сreate'] = 0
        data = users.loc[users['id'].values.tolist().index(message.from_user.id), 'VCScreate'].split(';')
        data[2] = int(data[2])
        data[3] = int(data[3])
        print(data)
        jsonlogin = {
            "login": str(users.loc[users['id'].values.tolist().index(message.from_user.id), 'login']),
            "password": str(users.loc[users['id'].values.tolist().index(message.from_user.id), 'password']),
            "fingerprint": {}
        }

        token = requests.post(url_login, headers=headers_login, json=jsonlogin).json()['token']

        headers = {
            'Authorization': 'Bearer ' + str(token),
            'Content-Type': 'application/json',
        }

        cre = {
            "name": data[0],
            "ciscoSettings": {
                "isMicrophoneOn": True,
                "isVideoOn": True,
                "isWaitingRoomEnabled": True
            },
            "participantsCount": data[1],
            "startedAt": data[2],
            "duration": data[3],
            "participants": [],
            "sendNotificationsAt": "2024-11-30T11:45:00",
            "state": "booked"
        }

        v = requests.post(url_vcs, headers=headers, json=cre)
        users.loc[users['id'].values.tolist().index(message.from_user.id), 'сreate'] = 0

        await message.answer(v.text)




async def main():
    await dp.start_polling(bot)


asyncio.run(main())