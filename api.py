import requests

url_vcs = 'https://test.vcc.uriit.ru/api/meetings'
url_login = 'https://test.vcc.uriit.ru/api/auth/login'


jsonlogin = {
    "login": 'hantaton08',
    "password": 'apyNbPS5Wr8^PbCg',
    "fingerprint": {}
}

headers_login = {'Content-Type': 'application/json'}
token = requests.post(url_login, headers=headers_login, json=jsonlogin).json()['token']
headers = {
    'Authorization': 'Bearer ' + token,
    'Content-Type': 'application/json'
}

params_vcs = {
    'fromDatetime': f'2024-11-26T22:12:39.191051',
    'toDatetime': f'2024-11-27T18:12:39.191114',
    'state': 'started'
}
vcs = requests.get('https://test.vcc.uriit.ru/api/meetings', headers=headers, params=params_vcs)

cre = {
    "name": "228",
    "ciscoSettings": {
        "isMicrophoneOn": True,
        "isVideoOn": True,
        "isWaitingRoomEnabled": True
    },
    "participantsCount": 5,
    "startedAt": "2025-01-08T12:00:00",
    "duration": 120,
    "participants": [],
    "sendNotificationsAt": "2024-11-30T11:45:00",
    "state": "booked"
}

v = requests.post(url_vcs, headers=headers, json=cre)

print(v)

# for i in vcs.json()['data']:
#     print(i['name'])
#
# print(vcs.json()['data'][0])