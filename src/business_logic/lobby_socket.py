from flask import g, redirect, request, url_for

from flask_socketio import emit

from src import kaku_app

from src.business_logic import global_state
from src.session_connection import authentication

socketio = kaku_app.socketio

def redirectOut(error_message):
    emit('Redirect Out')
    return error_message

def beforeAppRequest():
    authentication.load_logged_in_user()
    if g.player_name is None:
        return redirectOut("Credentials lost in the internet.")
    return

@socketio.event
def connectToLobby(data=None):
    player_sid = request.sid
    err = beforeAppRequest()
    if err is not None: # TODO: flash error
        redirectOut(err)
        return

    player_id = g.player_id

    if player_id in global_state.SESSIONS_TO_CAT_ROOM_IDS:
        redirectOut("You are already in a lobby/game.")
        return