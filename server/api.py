from flask import Flask, render_template, make_response, request
from flask_restful import Resource, Api
from flask_socketio import SocketIO
import logging
import Fiesta

app = Flask(__name__, template_folder= '../client/templates/')
log = logging.getLogger('werkzeug')
log.disabled = True
api = Api(app)
socketio = SocketIO(app)

fiesta = Fiesta.Fiesta()

# Sockets Handling
@socketio.on('connect')
def handle_connection():
    fiesta.add_connection(request.sid)

@socketio.on('disconnect')
def handle_disconnection():
    fiesta.remove_connection(request.sid)

@socketio.on('new_player')
def handle_new_player(data):
    print(data)
    fiesta.add_player(nickname = data['nickname'], sid = request.sid)
    print(fiesta.players)

# REST 
class Welcome(Resource):
    def get(self):
        return make_response(render_template('index.html'))

api.add_resource(Welcome, '/')

# Launch application
if __name__ == '__main__':
    socketio.run(app, debug = True)