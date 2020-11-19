from flask import Flask, render_template, make_response
from flask_restful import Resource, Api
from flask_socketio import SocketIO

app = Flask(__name__, template_folder= '../client/templates/')
api = Api(app)
socketio = SocketIO(app)

# Sockets
@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))

# REST
class Welcome(Resource):
    def get(self):
        return make_response(render_template('index.html'))

api.add_resource(Welcome, '/')


# Launch application
if __name__ == '__main__':
    socketio.run(app)
    #app.run(debug=True)