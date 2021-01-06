import eventlet
eventlet.monkey_patch()

import flask
app = flask.Flask(__name__)