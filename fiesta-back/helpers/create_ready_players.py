import requests
import random
import string

url = 'http://0.0.0.0:5000'

# Create 3 players
for i in range(3):
    sid = str(i)
    nickname = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
    payload = {'nickname': nickname, 'sid': sid}
    r = requests.post(url + '/api/create_player', json=payload)

# Set ready
for i in range(3):
    sid = str(i)
    payload = {'ready': True, 'sid': sid}
    r = requests.put(url + '/api/set_ready', json=payload)
