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

# Sockets Handling
@socketio.on('connect')
def handle_connection():
    socketio.emit('players', fiesta.players)
    fiesta.add_connection(request.sid)

@socketio.on('disconnect')
def handle_disconnection():
    fiesta.remove_connection(request.sid)

# REST 
@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/create_player', methods = ['POST'])
def create_player():
    fiesta.add_player(
        nickname = request.json['nickname'], 
        sid = request.json['sid'])
    socketio.emit('players', fiesta.players)
    return jsonify(nickname=request.json['nickname'], sid=request.json['sid'])

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

@app.route('/api/start_round', methods = ['GET'])
def start_round():
    fiesta.start_round()

@app.route('/api/send_word', methods = ['POST'])
def send_word():
    fiesta.add_word_from_sid(
        word = request.json['word'], 
        sid = request.json['sid'])
    if fiesta.check_if_all_words_submitted():
        socketio.emit('all_words_submitted')
        fiesta.current_turn += 1
    return jsonify(ready=request.json['word'], sid=request.json['sid'])

@app.route('/api/get_word', methods = ['POST'])
def get_word():
    word = fiesta.get_last_word_from_sid(
        sid = request.json['sid'])
    return jsonify(word = word, turn = fiest.current_turn)

@app.errorhandler(404)
def handle_404(e):
    if request.path.startswith('/api'):
        return _ , 404
    else:
        return redirect(url_for('index'))

# Launch application
if __name__ == '__main__':
    socketio.run(app, debug = True)