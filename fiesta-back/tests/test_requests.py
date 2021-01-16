import requests
from flask import jsonify
import json

url = 'http://0.0.0.0:5000'

def test_create_player():
    payload = {'nickname': 'alexis', 'sid': 2}
    r = requests.post(url + '/api/create_player', json=payload)
    assert r.status_code == 200
    assert 'nickname' in r.json()
    assert 'sid' in r.json()

def test_set_ready():
    payload = {'ready': True, 'sid': 2}
    r = requests.put(url + '/api/set_ready', json=payload)
    assert r.status_code == 200
    assert 'ready' in r.json()
    assert 'sid' in r.json()

def test_send_word():
    payload = {'word': 'sapin', 'sid': 2}
    r = requests.post(url + '/api/send_word', json=payload)
    assert r.status_code == 200
    assert 'ready' in r.json()
    assert 'sid' in r.json()

def test_get_word():
    payload = {'sid': 2}
    r = requests.post(url + '/api/get_word', json=payload)
    assert r.status_code == 200
    assert 'word' in r.json()
    assert 'turn' in r.json()

def test_get_character():
    payload = {'sid': 2}
    r = requests.post(url + '/api/get_character', json=payload)
    assert r.status_code == 200
    assert 'character' in r.json()

def test_get_all_characters():
    payload = {'sid': 2}
    r = requests.get(url + '/api/get_all_characters', json=payload)
    assert r.status_code == 200
    assert 'characters' in r.json()

def test_get_all_last_words():
    r = requests.get(url + '/api/get_all_last_words')
    assert r.status_code == 200
    assert 'last_words' in r.json()

def test_send_answers():
    payload = {
        'sid': 2, 
        'answers' : {
            'sapin' : 'character_01'
            }
        }
    r = requests.post(url + '/api/send_answers', json=payload)
    assert r.status_code == 200
    assert 'answers' in r.json()

def test_get_notebook():
    payload = {
        'last_word' : 'sapin'
        }
    r = requests.post(url + '/api/get_notebook', json=payload)
    assert r.status_code == 200

def test_consume_bone():
    payload = {
        'last_word' : 'sapin'
        }
    r = requests.post(url + '/api/consume_bone', json=payload)
    assert r.status_code == 200