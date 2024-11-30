import asyncio
from operator import index
from pyexpat.errors import messages
from datetime import datetime, timedelta

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
import json

url_vcs = 'https://test.vcc.uriit.ru/api/meetings'
url_login = 'https://test.vcc.uriit.ru/api/auth/login'

logging.basicConfig(level=logging.INFO)

bot = Bot(token='7897974325:AAE-G0xfOiwGaoNB-5mLoaCsd9pI-dHFrPo')
dp = Dispatcher()

headers_login = {'Content-Type': 'application/json'}

@dp.message(Command('start'))
async def StartLogin(message: Message):
    await message.answer('Привет! Для продолжения работы нужно авторизоваться')
    await message.answer('Для авторизации напишите /login логин пароль')
    await message.answer('Для просмотра списка команд введите /help')

@dp.message(Command('help'))
async def help(message: Message):
    users = pd.read_csv('log.csv')
    if np.int64(message.from_user.id) not in users['id'].values:
        await message.answer('Для того чтобы пользоватся ботом, вам нужно авторизоватся \nВведите /login логин пароль')
    else:
        await message.answer('/vcs - Просмотр всех вкс по заданным фильтрам\n/myvcs - Просмотр всех ВКС, в котором вы явдяетесь участником\n/create - Создание вкс')

@dp.message(Command('unlogin'))
async def unLogin(message: Message):
    users = pd.read_csv('log.csv')
    users.drop(users['id'].values.tolist().index(message.from_user.id), inplace=True)
    users.to_csv('log.csv', index=False)
    await message.answer('Вы вышли из свои учетной записи')


@dp.message(Command('login'))
async def asd(message: Message):
    users = pd.read_csv('log.csv')
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

            await message.answer(f'Вы успешно авторизовались!')

        except:
            await message.answer(ans['detail'] + '\nПопробуйте снова')
        users = pd.read_csv('log.csv')
    else:
        await message.answer('Вы авторизованы')


@dp.message(Command('vcs'))
async def VCSInfo(message: Message):
    users = pd.read_csv('log.csv')
    if np.int64(message.from_user.id) in users['id'].values:
        await message.answer('Введите даты начала и окончания ВКС через пробел, в формате: ГГГГ-ММ-ДД')

        try:
            data = str(message.text)[5:].split()

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

            nm = {
                'name': 'Название:',
                "startedAt": 'Начало: ',
                'endedAt': 'Конец',
                'duration': 'Продолжительность',
                'organizedBy': 'Организованно'
            }
            if len(vcs_ans) > 0:
                for i in vcs_ans:
                    try:
                        org = requests.get('https://test.vcc.uriit.ru/api/catalogs/departments/' + i['organizedBy'], headers=headers, params={'department_id': i['organizedBy']}).json()['name']
                        await message.answer(f'Название: {i['name']}\nДата начала: {i['startedAt'][:10]} {i['startedAt'][11:-3]}\nДата окончания: {i['endedAt'][:10]} {i['endedAt'][11:-3]}\nПродолжительность: {i['duration']} минут\nОрганизованно: {org}')
                    except:
                        await message.answer(f'Название: {i['name']}\nДата начала: {i['startedAt'][:10]} {i['startedAt'][11:-3]}\nДата окончания: {i['endedAt'][:10]} {i['endedAt'][11:-3]}\nПродолжительность: {i['duration']} минут')
            else:
                await message.answer('В этот период нет ВКС')

        except:
            await message.answer('Вы ввели некорректную дату')

@dp.message(Command('myvcs'))
async def myVCSInfo(message: Message):
    users = pd.read_csv('log.csv')

    if np.int64(message.from_user.id) in users['id'].values:
        users.loc[users['id'].values.tolist().index(message.from_user.id), 'create'] = 10
        # await message.answer('Введите даты начала и окончания ВКС через пробел, в формате: ГГГГ-ММ-ДД')
        try:
            data = str(message.text)[7:].split()
            print(1)
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

            vcs_ans = []
            info_vcs = ['name', 'startedAt', 'endedAt', 'duration', 'organizedBy']
            for i in ['started', 'ended', 'booked', 'cancelled']:
                id1 = requests.post(url_login, headers=headers_login, json=jsonlogin).json()['user']['id']
                params_vcs = {
                    'fromDatetime': f'{data[0]}T00:00:00.000000',
                    'toDatetime': f'{data[1]}T23:59:00.000000',
                    'state': i,
                    'userParticipant': int(id1)
                }
                vcs = requests.get(url_vcs, headers=headers, params=params_vcs)
                vcs_ans += vcs.json()['data']

            if len(vcs_ans) > 0:
                for i in vcs_ans:
                    try:
                        org = requests.get('https://test.vcc.uriit.ru/api/catalogs/departments/' + i['organizedBy'], headers=headers, params={'department_id': i['organizedBy']}).json()['name']
                        await message.answer(f'Название: {i['name']}\nДата начала: {i['startedAt'][:10]} {i['startedAt'][11:-3]}\nДата окончания: {i['endedAt'][:10]} {i['endedAt'][11:-3]}\nПродолжительность: {i['duration']} минут\nОрганизованно: {org}')
                    except:
                        await message.answer(f'Название: {i['name']}\nДата начала: {i['startedAt'][:10]} {i['startedAt'][11:-3]}\nДата окончания: {i['endedAt'][:10]} {i['endedAt'][11:-3]}\nПродолжительность: {i['duration']} минут')
            else:
                await message.answer('В этот период нет ВКС')
        except:
            await message.answer('Вы ввели некорректную дату')


@dp.message(Command('create'))
async def CreateVcs(message: Message):
    users = pd.read_csv('log.csv')
    if np.int64(message.from_user.id) in users['id'].values:
        users.loc[users['id'].values.tolist().index(message.from_user.id), 'create'] = 1
        users.to_csv('log.csv', index=False)
        await message.answer('Чтобы создать новую ВКС, введите название ВКС')

@dp.message(Command('cancel'))
async def CanсelVcs(message: Message):
    users = pd.read_csv('log.csv')
    users.loc[users['id'].values.tolist().index(message.from_user.id), 'create'] = 0

    users.to_csv('log.csv', index=False)
    await message.answer('Cоздание ВКС отменено')

@dp.message()
async def CreateVcs1(message: Message):
    users = pd.read_csv('log.csv')
    if np.int64(message.from_user.id) in users['id'].values:
        if users.loc[users['id'].values.tolist().index(message.from_user.id), 'create'] == 1:
            users.loc[users['id'].values.tolist().index(message.from_user.id), 'create'] = 2
            response = message.text
            users.loc[users['id'].values.tolist().index(message.from_user.id), 'VCScreate'] = response
            users.to_csv('log.csv', index=False)
            await message.answer('Введите время начала конференции (гггг-мм-дд чч:мм)')

        elif users.loc[users['id'].values.tolist().index(message.from_user.id), 'create'] == 2:
            users.loc[users['id'].values.tolist().index(message.from_user.id), 'create'] = 3

            response = message.text
            tmp = response.split()[1]
            response = response.replace(' ', f'T{tmp}:00.000000')[:-5]

            users.loc[users['id'].values.tolist().index(message.from_user.id), 'VCScreate'] = users.loc[users['id'].values.tolist().index(message.from_user.id), 'VCScreate'] + '$' + str(response)
            users.to_csv('log.csv', index=False)
            await message.answer('Введите максимальное кол-во участников конференции')

        elif users.loc[users['id'].values.tolist().index(message.from_user.id), 'create'] == 3:
            users.loc[users['id'].values.tolist().index(message.from_user.id), 'create'] = 4

            response = message.text
            users.loc[users['id'].values.tolist().index(message.from_user.id), 'VCScreate'] += '$' + response
            users.to_csv('log.csv', index=False)
            await message.answer('Введите продoлжительность конференции в минутах')

        elif users.loc[users['id'].values.tolist().index(message.from_user.id), 'create'] == 4:
            users.loc[users['id'].values.tolist().index(message.from_user.id), 'create'] = 5
            response = message.text
            users.loc[users['id'].values.tolist().index(message.from_user.id), 'VCScreate'] += '$' + response
            users.to_csv('log.csv', index=False)
            await message.answer('''Отправтье любое сообщение для подтверждения создания ВКС''')

        elif users.loc[users['id'].values.tolist().index(message.from_user.id), 'create'] == 5:
            users.loc[users['id'].values.tolist().index(message.from_user.id), 'create'] = 0
            zxc = users.loc[users['id'].values.tolist().index(message.from_user.id), 'VCScreate'].split('$')
            # users.loc[users['id'].values.tolist().index(message.from_user.id), 'VCScreate'] = ''
            users.to_csv('log.csv', index=False)
            print(zxc)
            if len(zxc) >= 4:
                try:
                    zxc[2] = int(zxc[2])
                    zxc[3] = int(zxc[3])
                except ValueError:
                    await message.answer('Ошибка при преобразовании данных. Убедитесь, что время и продолжительность указаны верно.')
                    return
            else:
                await message.answer('Недостаточно данных для создания события.')
                return

            jsonlogin = {
                "login": str(users.loc[users['id'].values.tolist().index(message.from_user.id), 'login']),
                "password": str(users.loc[users['id'].values.tolist().index(message.from_user.id), 'password']),
                "fingerprint": {}
            }

            try:
                response = requests.post(url_login, headers=headers_login, json=jsonlogin)
                response.raise_for_status()
                token = response.json().get('token')
                if not token:
                    return
            except requests.exceptions.RequestException as e:
                print(e)
                return

            headers = {
                'Authorization': 'Bearer ' + str(token),
                'Content-Type': 'application/json',
            }
            print(zxc[1])

            started_at_str = zxc[1]
            started_at = datetime.strptime(started_at_str, "%Y-%m-%dT%H:%M:%S.%f")
            send_notifications_at = started_at - timedelta(hours=1)
            started_at1 = started_at - timedelta(hours=5)

            started_at1str = started_at1.strftime("%Y-%m-%dT%H:%M:%S")
            send_notifications_at_str = send_notifications_at.strftime("%Y-%m-%dT%H:%M:%S")
            participants_count = int(zxc[2])

            h = int(zxc[1][11:13]) - 5

            if h < 0:
                d = int(zxc[1][8:10])
                d -= 1
                d = str(d)
                h = 24 + h
                zxc[1] = zxc[1][:8] + d + zxc[1][10:11] + str(h) + zxc[1][13:]

            if (h > 0 and h < 10):
                h = '0' + str(h)
            zxc[1] = zxc[1][:11] + str(h) + zxc[1][13:]
            print(zxc[1])

            cre = {
                "name": zxc[0],
                "ciscoSettings": {
                    "isMicrophoneOn": True,
                    "isVideoOn": True,
                    "isWaitingRoomEnabled": True
                },
                "participantsCount": participants_count,
                "startedAt": zxc[1],
                "duration": zxc[3],
                "participants": [],
                "sendNotificationsAt": send_notifications_at_str,
                "state": "booked",
                "organizedBy":{
                    'id': requests.post(url_login, headers=headers_login, json=jsonlogin).json()['user']['id']
                }
            }

            try:
                v = requests.post(url_vcs, headers=headers, json=cre)
                v.raise_for_status()

                await message.answer(f'ВКС успешно создана \nСсылка для подключения {v.json()['permalink']}')

            except requests.exceptions.RequestException as e:
                # await message.answer("Произошла ошибка при создании ВКС, попробуйте заново.")
                pass

        elif users.loc[users['id'].values.tolist().index(message.from_user.id), 'create'] == 2:
            await message.answer('Введите дату начала')
    else:
        await message.answer('Пожалуйста авторизуйтесь /login логин пароль')




async def main():
    await dp.start_polling(bot)


asyncio.run(main())