# Entry point for the application.
from os import environ

from dotenv import load_dotenv
from flask import request, session
from flask_socketio import SocketIO

from . import app  # For application discovery by the 'flask' command.

load_dotenv('.env')

app.config.from_mapping(
    SECRET_KEY=environ.get('SECRET_KEY'), 
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax'
    #TODO: make the app https, so that we can use SESSION_COOKIE_SECURE=True
)

from . import home_page
from . import sekai_and_category

app.register_blueprint(home_page.bp)
app.register_blueprint(sekai_and_category.bp)

socketio = SocketIO(app, async_mode='eventlet')

@socketio.on('connect')
def handle_message(data=None):
    print('connected')
    print(request.sid)
    print(session.get('player_name'))

@socketio.event
def sayHi(data=None):
    print(data['one'])

if __name__ == '__main__':
    socketio.run(app)
