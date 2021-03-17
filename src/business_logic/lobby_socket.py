import logging
import time
import uuid

from flask import g, redirect, request, url_for
from flask_socketio import emit, join_room
from src import kaku_app
from src.business_logic import game_definitions, global_state, lobby_logic
from src.helpers import common_helpers, data_integrity
from src.session_connection import authentication

socketio = kaku_app.socketio

def redirectOutLobby(error_message):
    emit('Redirect Out')


def warningLobby(warning_message):
    emit('Warning')


def sendInitialStatus(lobby_conf, is_host):
    player_slots = [None, None, None, None, None, None, None, None, None, None]

    game_settings = lobby_conf['game_settings']
    game_settings_version = game_settings.get('version')
    game_type = None
    game_difficulty = None
    game_topic = None
    game_filters = None
    if not is_host:
        game_type = game_settings.get('game_type')
        game_type = game_definitions.SERIALIZE_GAME_DEFINITIONS[game_type]

        game_difficulty = game_settings.get('difficulty')
        game_difficulty = game_definitions.SERIALIZE_GAME_DIFFICULTY[game_difficulty]

        game_topic = game_settings.get('topic')

        game_filters = [filter.attribute for filter in game_settings.get('filters')]

    for pos in lobby_conf['players_slots']:
        player_slot = lobby_conf['players_slots'][pos]
        if player_slot is not None:
            player_slot = player_slot.get('player_name')
        player_slots[pos] = player_slot
    emit('Initial Status', {'player_slots':player_slots,
                            'game_settings_version':game_settings_version,
                            'game_type':game_type,
                            'game_difficulty':game_difficulty,
                            'game_topic':game_topic,
                            'game_filters':game_filters})


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
        warningLobby("Can't send lobby messages when the game already started.")
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
        return

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
            redirectOutLobby("How did you get here so fast? The host isn't even here yet.")
            return

        synchro_id = str(uuid.uuid4())
        global_state.SOCKETS_TO_SESSIONS[player_sid] = player_id
        global_state.SESSIONS_TO_CAT_ROOM_IDS[player_id] = (room_id, category_name, synchro_id)

        time.sleep(1.2)
        if player_id not in global_state.SESSIONS_TO_CAT_ROOM_IDS or global_state.SESSIONS_TO_CAT_ROOM_IDS[player_id][2]!=synchro_id:
            del global_state.SOCKETS_TO_SESSIONS[player_sid]
            redirectOutLobby("Looks like the internet is not waiting for us.")
            return

        if 'garbage_collector' not in lobby_conf:
            del global_state.SOCKETS_TO_SESSIONS[player_sid]
            del global_state.SESSIONS_TO_CAT_ROOM_IDS[player_id]
            redirectOutLobby("Looks like the internet is confused with your requests.")
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

        sendInitialStatus(lobby_conf, is_host)

        global_state.SESSIONS_TO_CAT_ROOM_IDS[player_id] = (room_id, category_name, None)
        
        emit('Successful Connection')
    elif lobby.lobby_nature == lobby_logic.LobbyNature.IN_LOBBY:
        if is_host:
            redirectOutLobby("Uhm. Aren't you the host of this lobby?")
            return

        if data_integrity.dictIsCorrupted(['players_slots', 'players_synchro', 'slots_synchro'], lobby_conf):
            redirectOutLobby("The data was corrupted :c. Please reload the page.")
            return
        synchro_id = str(uuid.uuid4())

        pos = 0
        for i in range(1, 10):
            if lobby_conf['players_slots'][i] is None and lobby_conf['slots_synchro'][i] is None:
                pos = i
                lobby_conf['slots_synchro'][pos] = synchro_id
                break
        if pos == 0:
            redirectOutLobby("Somebody was quicker, the lobby is sadly full. Try again later or try joining another lobby.")
            return

        global_state.SOCKETS_TO_SESSIONS[player_sid] = player_id
        global_state.SESSIONS_TO_CAT_ROOM_IDS[player_id] = (room_id, category_name, synchro_id)
        
        time.sleep(1.2) # TODO: Make this a parameter of this file.

        if lobby_conf['slots_synchro'][pos]!=synchro_id or lobby_conf['players_slots'][pos] is not None:
            del global_state.SOCKETS_TO_SESSIONS[player_sid]
            if global_state.SESSIONS_TO_CAT_ROOM_IDS[player_id][2]==synchro_id:
                del global_state.SESSIONS_TO_CAT_ROOM_IDS[player_id]
            redirectOutLobby("Looks like the internet is not waiting for us.")
            return
        
        if player_id not in global_state.SESSIONS_TO_CAT_ROOM_IDS or global_state.SESSIONS_TO_CAT_ROOM_IDS[player_id][2]!=synchro_id:
            del global_state.SOCKETS_TO_SESSIONS[player_sid]
            lobby_conf['slots_synchro'][pos] = None
            redirectOutLobby("Looks like the internet is not waiting for us.")
            return

        # TODO: Check if the game is meant to start.

        lobby_conf['players_synchro'].append(synchro_id)
        
        join_room(room_id)
        _res, error = lobby.playerJoinLobby(player_sid, player_id, g.player_name, pos)
        if error is not None:
            del global_state.SOCKETS_TO_SESSIONS[player_sid]
            del global_state.SESSIONS_TO_CAT_ROOM_IDS[player_id]
            lobby_conf['slots_synchro'][pos] = None
            lobby_conf['players_synchro'].remove(synchro_id)
            redirectOutLobby(error)
            return

        socketio.emit('New Player Join', {'player_name':g.player_name, 'pos':pos}, room=room_id)

        sendInitialStatus(lobby_conf, is_host)
        
        global_state.SESSIONS_TO_CAT_ROOM_IDS[player_id] = (room_id, category_name, None)
        lobby_conf['slots_synchro'][pos] = None
        lobby_conf['players_synchro'].remove(synchro_id)
        
        emit('Successful Connection')
    else:
        redirectOutLobby("The lobby you tried to join was not ready for you.")
        return


    print("### in lobby_socket.py ###")
    print('player_sid : room_id #', global_state.SOCKETS_TO_SESSIONS)
    print('session : room_id #', global_state.SESSIONS_TO_CAT_ROOM_IDS)
    print('cat_room_id : lobby #', global_state.CAT_ROOM_IDS_TO_LOBBIES)
