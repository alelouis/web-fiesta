from flask import Flask, render_template, make_response, request, redirect, url_for, jsonify
from flask_restful import Resource, Api
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import logging
import Fiesta

app = Flask(__name__, static_folder='static/', static_url_path='/')
log = logging.getLogger('werkzeug')
log.disabled = True
api = Api(app)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

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
    fiesta.add_player(
        nickname = request.json['nickname'], 
        sid = request.json['sid'])
    socketio.emit('players', fiesta.players)
    return jsonify(nickname=request.json['nickname'], sid=request.json['sid'])

""" set a player's ready status """
@app.route('/api/set_ready', methods = ['PUT'])
def set_ready():
    fiesta.set_ready(
        ready = request.json['ready'], 
        sid = request.json['sid'])
    socketio.emit('players', fiesta.players)
    if fiesta.check_if_all_ready():
        fiesta.start_round()
        socketio.emit('all_ready', {})
    return jsonify(ready=request.json['ready'], sid=request.json['sid'])

""" send_word, cycle notebooks """
@app.route('/api/send_word', methods = ['POST'])
def send_word():
    fiesta.add_word_from_sid(
        word = request.json['word'], 
        sid = request.json['sid'])
    if fiesta.check_if_all_words_submitted():
        socketio.emit('all_words_submitted')
        fiesta.cycle_notebooks()
        fiesta.current_turn += 1
        if fiesta.check_rotation_completed():
            socketio.emit('rotation_completed')
            
    return jsonify(ready=request.json['word'], sid=request.json['sid'])

""" get last word from notebook """
@app.route('/api/get_word', methods = ['POST'])
def get_word():
    word = fiesta.get_last_word_from_sid(
        sid = request.json['sid'])
    return jsonify(word = word, turn = fiesta.current_turn)

""" get character from notebook """
@app.route('/api/get_character', methods = ['POST'])
def get_character():
    word = fiesta.get_character(
        sid = request.json['sid'])
    return jsonify(character = character)

# Launch application
if __name__ == '__main__':
    socketio.run(app, debug = True)