import logging
import time
import uuid

from flask import g, redirect, request, url_for
from flask_socketio import emit, join_room
from src import kaku_app
from src.business_logic import global_state, lobby_logic
from src.helpers import common_helpers, data_integrity
from src.session_connection import authentication

socketio = kaku_app.socketio

def redirectOutLobby(error_message):
    emit('Redirect Out')
    return error_message


def warningLobby(warning_message):
    emit('Warning')
    return warning_message


def beforeAppRequest():
    authentication.load_logged_in_user()
    if g.player_name is None:
        return "Credentials lost in the internet."
    return


def retrievePlayerContext(player_sid):
    error = None
    if player_sid not in global_state.SOCKETS_TO_SESSIONS:
        error = "Credentials lost in the internet."
        return None, None, None, error

    player_id = global_state.SOCKETS_TO_SESSIONS[player_sid]
    if g.player_id != player_id:
        error = "Credentials lost in the internet."
        return None, None, None, error

    if player_id not in global_state.SESSIONS_TO_CAT_ROOM_IDS:
        error = "Credentials lost in the internet."
        return None, None, None, error
    room_id, category_name, _synchro_id = global_state.SESSIONS_TO_CAT_ROOM_IDS[player_id]

    return  player_id, category_name, room_id, error


@socketio.event
def sendLobbyMessage(data=None):
    err = beforeAppRequest()
    if err is not None: # TODO: flash error
        redirectOutLobby(err)
        return

    if 'text_to_send' not in data:
        redirectOutLobby("Something happened with your data.")
        return

    text_to_send = str(data.get('text_to_send'))
    player_sid = request.sid
    _player_id, _category_name, room_id, err = retrievePlayerContext(player_sid)
    if err is not None: # TODO: flash error
        redirectOutLobby(err)
        return

    player_name = g.player_name

    lobby = common_helpers.retrieveRoomFromID(room_id)
    if lobby is None:
        redirectOutLobby("Lobby not found in the internet.")
        return

    if lobby.lobby_nature != lobby_logic.LobbyNature.IN_LOBBY:
        warningLobby("Can't send messages when the lobby is already in game.")
        return

    socketio.emit('Receive Lobby Message', {'sender_name':player_name, 'text_sent':text_to_send}, room=room_id)


@socketio.event
def connectToLobby(data=None):
    err = beforeAppRequest()
    if err is not None: # TODO: flash error
        redirectOutLobby(err)
        return

    if 'room_id' not in data:
        redirectOutLobby("Something happened with your data.")
        return

    player_sid = request.sid
    room_id = str(data.get('room_id'))

    lobby = common_helpers.retrieveRoomFromID(room_id)

    if lobby is None:
        redirectOutLobby("Lobby not found in the internet.")
        return

    lobby_conf = lobby.lobby_conf
    if data_integrity.dictIsCorrupted(['category_name', 'host_id'], lobby_conf):
        redirectOutLobby("The data was corrupted :c. Please reload the page.")

    player_id = g.player_id
    host_id = lobby_conf['host_id']
    category_name = lobby_conf['category_name']

    is_host = False
    if host_id == player_id:
        is_host = True

    # Here comes the synchro critical section.
    if player_id in global_state.SESSIONS_TO_CAT_ROOM_IDS:
        redirectOutLobby("You are already in a lobby/game.")
        return

    if lobby.lobby_nature == lobby_logic.LobbyNature.CREATE_LOBBY:
        if not is_host:
            redirectOutLobby("How did you get here this fast? The host isn't even here yet.")
            return

        synchro_id = str(uuid.uuid4())
        global_state.SOCKETS_TO_SESSIONS[player_sid] = player_id
        global_state.SESSIONS_TO_CAT_ROOM_IDS[player_id] = [room_id, category_name, synchro_id]

        time.sleep(1.4)
        if player_id not in global_state.SESSIONS_TO_CAT_ROOM_IDS or global_state.SESSIONS_TO_CAT_ROOM_IDS[player_id][2]!=synchro_id:
            del global_state.SOCKETS_TO_SESSIONS[player_sid]
            redirectOutLobby("Looks like the internet is not waiting for us.")
            return

        if 'garbage_collector' not in lobby_conf:
            del global_state.SOCKETS_TO_SESSIONS[player_sid]
            del global_state.SESSIONS_TO_CAT_ROOM_IDS[player_id]
            redirectOutLobby("Looks like the internet is not waiting for us.")
            return

        garbage_collector = lobby_conf['garbage_collector']
        garbage_collector.cancel()
        time.sleep(0.3)

        if garbage_collector.is_alive() or common_helpers.retrieveRoomFromID(room_id) is None:
            del global_state.SOCKETS_TO_SESSIONS[player_sid]
            del global_state.SESSIONS_TO_CAT_ROOM_IDS[player_id]
            redirectOutLobby("Looks like the internet is not waiting for us.")
            return

        del lobby_conf['garbage_collector']

        lobby_params = {'player_sid' : player_sid}

        join_room(room_id)
        _res, _error = lobby.setLobbyNature(lobby_logic.LobbyNature.IN_LOBBY, lobby_params)
        global_state.SESSIONS_TO_CAT_ROOM_IDS[player_id][2] = None
        print("$$$$")
        print(global_state.SESSIONS_TO_CAT_ROOM_IDS[player_id])
        
        emit('Successful Connection')

    print("### in lobby_socket.py ###")
    print('player_sid : room_id #', global_state.SOCKETS_TO_SESSIONS)
    print('session : room_id #', global_state.SESSIONS_TO_CAT_ROOM_IDS)
    print('cat_room_id : lobby #', global_state.CAT_ROOM_IDS_TO_LOBBIES)
