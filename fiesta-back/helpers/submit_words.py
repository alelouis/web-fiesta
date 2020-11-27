import requests
import random
import string

url = 'http://127.0.0.1:5000'
# Add words
for sid in range(3):
    word =''.join(random.choice(string.ascii_lowercase) for i in range(5))
    payload = {'word': word, 'sid': str(sid)}
    r = requests.post(url + '/api/send_word', json=payload)