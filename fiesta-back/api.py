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
fiesta = Fiesta.Fiesta()

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

""" creates a player """
@app.route('/api/create_player', methods = ['POST'])
def create_player():
    log.info('Received POST on endpoint /api/create_player.')
    fiesta.add_player(
        nickname = request.json['nickname'], 
        sid = request.json['sid'])
    log.info("Emit event 'players'.")
    socketio.emit('players', fiesta.players)
    return jsonify(nickname=request.json['nickname'], sid=request.json['sid'])

""" set a player's ready status """
@app.route('/api/set_ready', methods = ['PUT'])
def set_ready():
    log.info('Received PUT on endpoint /api/set_ready.')
    fiesta.set_ready(
        ready = request.json['ready'], 
        sid = request.json['sid'])
    socketio.emit('players', fiesta.players)
    if fiesta.check_if_all_ready():
        fiesta.start_round()
        log.info("Emit event 'all_ready'.")
        socketio.emit('all_ready')
    return jsonify(ready=request.json['ready'], sid=request.json['sid'])

""" send_word, cycle notebooks """
@app.route('/api/send_word', methods = ['POST'])
def send_word():
    log.info('Received POST on endpoint /api/send_word.')
    fiesta.add_word_from_sid(
        word = request.json['word'], 
        sid = request.json['sid'])
    if fiesta.check_if_all_words_submitted():
        log.info("Emit event 'all_words_submitted'.")
        socketio.emit('all_words_submitted')
        fiesta.cycle_notebooks()
        fiesta.current_turn += 1
        if fiesta.check_rotation_completed():
            log.info("Emit event 'rotation_completed'.")
            socketio.emit('rotation_completed')
            
    return jsonify(ready=request.json['word'], sid=request.json['sid'])

""" get last word from notebook """
@app.route('/api/get_word', methods = ['POST'])
def get_word():
    log.info('Received POST on endpoint /api/get_word.')
    word = fiesta.get_last_word_from_sid(
        sid = request.json['sid'])
    return jsonify(word = word, turn = fiesta.current_turn)

""" get character from notebook """
@app.route('/api/get_character', methods = ['POST'])
def get_character():
    log.info('Received POST on endpoint /api/get_character.')
    character = fiesta.get_character(
        sid = request.json['sid'])
    return jsonify(character = character)

""" get the 8 characters """
@app.route('/api/get_all_characters', methods = ['GET'])
def get_all_characters():
    log.info('Received GET on endpoint /api/get_all_characters.')
    characters = fiesta.get_all_characters()
    random.shuffle(characters)
    return jsonify(characters = characters)

""" get the last words of notebooks """
@app.route('/api/get_all_last_words', methods = ['GET'])
def get_all_last_words():
    log.info('Received GET on endpoint /api/get_all_last_words.')
    last_words = fiesta.get_all_last_words()
    random.shuffle(last_words)
    return jsonify(last_words = last_words)

""" processing answers """
@app.route('/api/send_answers', methods = ['POST'])
def send_answers():
    log.info('Received POST on endpoint /api/send_answers.')
    fiesta.process_answers(
        sid = request.json['sid'],
        answers = request.json['answers'])
    if fiesta.check_if_all_answers_submitted():
        log.info("Emit event 'all_answers_submitted'.")
        socketio.emit('all_answers_submitted')
    return jsonify(answers = request.json['answers'], sid = request.json['sid'])

""" compute correction and broadcast notebook history """
@app.route('/api/get_notebook', methods = ['POST'])
def get_notebook():
    log.info('Received POST on endpoint /api/get_notebook.')
    notebook = fiesta.get_notebook_from_last_word(request.json['last_word'])
    corrections = fiesta.get_corrections(notebook)
    fiesta.check_if_all_answers_are_correct(corrections)
    log.info("Emit event 'notebook'.")
    socketio.emit('notebook', {
        'word_list': notebook.words, 
        'corrections': corrections})
    socketio.emit('bones', {'bones': fiesta.bones})
    return Response(status=200)

""" removes a bone from the game """
@app.route('/api/consume_bone', methods = ['GET'])
def consume_bone():
    log.info('Received GET on endpoint /api/consume_bone.')
    fiesta.remove_bone()
    socketio.emit('bones', {'bones': fiesta.bones})
    return Response(status=200)

""" clears game state """
@app.route('/api/clear_game', methods = ['GET'])
def clear_game():
    log.info('Received GET on endpoint /api/clear_game.')
    fiesta.clear_game()
    log.info("Emit event 'clear_game'.")
    log.info("Emit event 'players'.")
    socketio.emit('clear_game')
    socketio.emit('players', fiesta.players)
    return jsonify(cleared = True)

# Launch application
#if __name__ == '__main__':
#    socketio.run(app, debug = True, host = '0.0.0.0')
