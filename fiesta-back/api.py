from flask import Flask, render_template, make_response, request, redirect, url_for, jsonify, Response
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import random
import logging
import Fiesta
import sys

# Initialization
app = Flask(__name__, static_folder='static/', static_url_path='/')
log = logging.getLogger('werkzeug')
log.disabled = True
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

# Logging
log = logging.getLogger("api")
formatter = logging.Formatter('%(asctime)s - %(name)8s - [%(levelname)s] %(message)s')

fh = logging.FileHandler('logs/api.log')
fh.setFormatter(formatter)
fh.setLevel(logging.DEBUG)

log.addHandler(fh)
log.setLevel(logging.DEBUG)

# Game instance
fiestas = {}

# main endpoints

""" main route """
@app.route('/')
def index():
    return app.send_static_file('index.html')

""" redirect all endpoints expect /api/ to index.html """
@app.errorhandler(404)
def handle_404(e):
    if request.path.startswith('/api'):
        return _ , 404
    else:
        return redirect(url_for('index'))

# api

""" creates a room and associated fiesta object """
@app.route('/api/create_room', methods = ['POST'])
def create_room():
    print("Room created")
    room_id = request.json['room_id']
    log.info('Received POST on endpoint /api/create_player.')
    fiestas.update({room_id : Fiesta.Fiesta()})
    log.info(f"Created new room with id {room_id}")
    return Response(status=200)

""" creates a player """
@app.route('/api/<room_id>/create_player', methods = ['POST'])
def create_player(room_id):
    log.info('Received POST on endpoint /api/create_player.')
    fiesta = fiestas[room_id]
    fiesta.add_player(
        nickname = request.json['nickname'], 
        sid = request.json['sid'])
    log.info("Emit event 'players'.")
    socketio.emit('players', fiesta.players)
    return Response(status=200)

""" set a player's ready status """
@app.route('/api/<room_id>/set_ready', methods = ['PUT'])
def set_ready(room_id):
    log.info('Received PUT on endpoint /api/set_ready.')
    fiesta = fiestas[room_id]
    fiesta.set_ready(
        ready = request.json['ready'], 
        sid = request.json['sid'])
    socketio.emit('players', fiesta.players)
    if fiesta.check_if_all_ready():
        fiesta.start_round()
        log.info("Emit event 'all_ready'.")
        socketio.emit('all_ready', {'contraints': fiesta.constraints})
    return Response(status=200)

""" send_word, cycle notebooks """
@app.route('/api/<room_id>/send_word', methods = ['POST'])
def send_word(room_id):
    log.info('Received POST on endpoint /api/send_word.')
    fiesta = fiestas[room_id]
    fiesta.add_word_from_sid(
        word = request.json['word'], 
        sid = request.json['sid'])

    fiesta.set_turn_ready(
        ready = True, 
        sid = request.json['sid'])
    socketio.emit('players', fiesta.players)

    if fiesta.check_if_all_words_submitted():
        log.info("Emit event 'all_words_submitted'.")
        socketio.emit('all_words_submitted')
        fiesta.cycle_notebooks()
        fiesta.current_turn += 1
        if fiesta.check_rotation_completed():
            log.info("Emit event 'rotation_completed'.")
            socketio.emit('rotation_completed')
    return Response(status=200)

""" get last word from notebook """
@app.route('/api/<room_id>/get_word', methods = ['POST'])
def get_word(room_id):
    fiesta = fiestas[room_id]
    log.info('Received POST on endpoint /api/get_word.')
    word = fiesta.get_last_word_from_sid(
        sid = request.json['sid'])
    return jsonify(word = word, turn = fiesta.current_turn)

""" get character from notebook """
@app.route('/api/<room_id>/get_character', methods = ['POST'])
def get_character(room_id):
    fiesta = fiestas[room_id]
    log.info('Received POST on endpoint /api/get_character.')
    character = fiesta.get_character(
        sid = request.json['sid'])
    return jsonify(character = character)

""" get the 8 characters """
@app.route('/api/<room_id>/get_all_characters', methods = ['GET'])
def get_all_characters(room_id):
    fiesta = fiestas[room_id]
    log.info('Received GET on endpoint /api/get_all_characters.')
    characters = fiesta.get_all_characters()
    random.shuffle(characters)
    return jsonify(characters = characters)

""" get the last words of notebooks """
@app.route('/api/<room_id>/get_all_last_words', methods = ['GET'])
def get_all_last_words(room_id):
    fiesta = fiestas[room_id]
    log.info('Received GET on endpoint /api/get_all_last_words.')
    last_words = fiesta.get_all_last_words()
    random.shuffle(last_words)
    return jsonify(last_words = last_words)

""" processing answers """
@app.route('/api/<room_id>/send_answers', methods = ['POST'])
def send_answers(room_id):
    fiesta = fiestas[room_id]
    log.info('Received POST on endpoint /api/send_answers.')
    fiesta.process_answers(
        sid = request.json['sid'],
        answers = request.json['answers'])
    if fiesta.check_if_all_answers_submitted():
        log.info("Emit event 'all_answers_submitted'.")
        socketio.emit('all_answers_submitted')
    return Response(status=200)

""" compute correction and broadcast notebook history """
@app.route('/api/<room_id>/get_notebook', methods = ['POST'])
def get_notebook(room_id):
    fiesta = fiestas[room_id]
    log.info('Received POST on endpoint /api/get_notebook.')
    notebook = fiesta.get_notebook_from_last_word(request.json['last_word'])
    corrections = fiesta.get_corrections(notebook)
    log.info("Emit event 'notebook'.")
    socketio.emit('notebook', {
        'word_list': notebook.words, 
        'corrections': corrections, 
        'correct_answers': notebook.correct_answers})
    socketio.emit('bones', {'bones': fiesta.bones})
    return Response(status=200)

""" removes a bone from the game """
@app.route('/api/<room_id>/consume_bone', methods = ['POST'])
def consume_bone(room_id):
    fiesta = fiestas[room_id]
    log.info('Received POST on endpoint /api/consume_bone.')
    fiesta.remove_bone()
    notebook = fiesta.get_notebook_from_last_word(request.json['last_word'])
    notebook.correct_answers += 1
    socketio.emit('notebook', {'correct_answers': notebook.correct_answers})
    socketio.emit('bones', {'bones': fiesta.bones})
    return Response(status=200)

""" clears game state """
@app.route('/api/<room_id>/clear_game', methods = ['GET'])
def clear_game(room_id):
    fiesta = fiestas[room_id]
    log.info('Received GET on endpoint /api/clear_game.')
    fiesta.clear_game()
    log.info("Emit event 'clear_game'.")
    log.info("Emit event 'players'.")
    socketio.emit('clear_game')
    socketio.emit('players', fiesta.players)
    return Response(status=200)

#Launch application
if __name__ == '__main__':
    socketio.run(app, debug = True, host = '0.0.0.0')
