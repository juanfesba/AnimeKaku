# Entry point for the application.
from . import app    # For application discovery by the 'flask' command.
from . import routing  # For import side-effects of setting up routes.
from flask_socketio import SocketIO
import os

app.config.from_mapping(
    SECRET_KEY=os.environ.get('SECRET_KEY')
)

socketio = SocketIO(app)
if __name__ == '__main__':
    socketio.run(app)