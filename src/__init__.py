import eventlet
eventlet.monkey_patch(socket=True)

import flask
app = flask.Flask(__name__)