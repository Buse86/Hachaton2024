import requests

url_event = 'https://test.vcc.uriit.ru/api/meetings'
url_login = 'https://test.vcc.uriit.ru/api/auth/login'
url_vcs = 'https://test.vcc.uriit.ru/api/meetings'

json_login = {
  "login": "hantaton08",
  "password": "apyNbPS5Wr8^PbCg",
  "fingerprint": {}
}

headers_login = {'Content-Type': 'application/json'}

token = requests.post(url_login, headers=headers_login, json=json_login).json()['token']

headers = {
    'Authorization': 'Bearer ' + token,
    'Content-Type': 'application/json'
}

event = requests.get(url_event, headers=headers)

params_vcs = {
    'fromDatetime': '2024-11-14T00:23:10.028081',
    'toDatetime': '2024-11-14T20:23:10.028122'
}

info_vcs = ['name', 'startedAt', 'endedAt', 'duration', 'organizedBy', ]

vcs = requests.get(url_vcs, headers=headers, params=params_vcs)

print(vcs.json()['data'])