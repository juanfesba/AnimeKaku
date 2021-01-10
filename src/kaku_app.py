# Entry point for the application.
from . import app    # For application discovery by the 'flask' command.
from flask_socketio import SocketIO
import os

app.config.from_mapping(
    SECRET_KEY=os.environ.get('SECRET_KEY')
)

from . import home_page
app.register_blueprint(home_page.bp)

socketio = SocketIO(app, async_mode='eventlet')
if __name__ == '__main__':
    socketio.run(app)