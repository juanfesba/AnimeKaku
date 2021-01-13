# Entry point for the application.
from . import app    # For application discovery by the 'flask' command.
from flask_socketio import SocketIO
from dotenv import load_dotenv
from os import environ

load_dotenv('.env')

app.config.from_mapping(
    SECRET_KEY=environ.get('SECRET_KEY'),
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)

from . import home_page
app.register_blueprint(home_page.bp)

socketio = SocketIO(app, async_mode='eventlet')
if __name__ == '__main__':
    socketio.run(app)