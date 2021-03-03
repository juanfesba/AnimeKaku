from flask import request, session

from src import kaku_app

socketio = kaku_app.socketio

@socketio.event
def connectToLobby(data=None):
    print(request.sid)
    print(session.get('player_id'))