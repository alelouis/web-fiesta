import requests
import random
import string

url = 'http://127.0.0.1:5000'
# Add words
for sid in range(3):
    last_words = requests.get(url + '/api/get_all_last_words').json()['last_words']
    characters = requests.get(url + '/api/get_all_characters').json()['characters']
    answers = {}
    for last_word in last_words:
        answers[last_word] = random.choice(characters)
    payload = {'answers': answers, 'sid': str(sid)}
    r = requests.post(url + '/api/send_answers', json=payload)