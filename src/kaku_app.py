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
from . import lobby

app.register_blueprint(home_page.bp)
app.register_blueprint(sekai_and_category.bp)
app.register_blueprint(lobby.bp)

socketio = SocketIO(app, async_mode='eventlet')

'''
@socketio.on('disconnect')
def handle_message(data=None):
    print(request.sid)
    print(session.get('player_name'))
'''

from src.business_logic import lobby_socket

if __name__ == '__main__':
    socketio.run(app)
