import threading
import uuid

from src.business_logic import global_state
from enum import Enum

def destroyUnusedLobby(room_id, category_name):
    if category_name in global_state.CAT_ROOM_IDS_TO_LOBBIES:
        rooms_in_category = global_state.CAT_ROOM_IDS_TO_LOBBIES[category_name]
        if room_id in rooms_in_category:
            del rooms_in_category[room_id]

    # del global_state.SESSIONS_TO_CAT_ROOM_IDS[host_id]

class LobbyNature(Enum):
    NONE = 0
    CREATE_LOBBY = 1
    AFTER_GAME = 2
    IN_LOBBY = 3
    IN_GAME = 4

class LobbySynchro(Enum):
    NONE = 0
    STARTING_LOBBY = 1
    JOINING_LOBBY = 2
    LEAVING_LOBBY = 3

'''
### lobby_conf ###

# General (CREATE_LOBBY) #

lobby_name
category_name
host_id

garbage_collector

# In lobby (IN_LOBBY) #

critical_synchro
is_private
password

@ players - key = pos

player_id
player_name
player_sid

@ game_settings

type
topic
difficulty
filters

'''

class Lobby():
    
    def __init__(self):
        self.room_id = str(uuid.uuid4())
        self.lobby_nature = LobbyNature.NONE
        self.lobby_conf = dict()

    def setLobbyNature(self, lobby_nature, lobby_conf):
        error = False
        res = None
        if lobby_nature == LobbyNature.CREATE_LOBBY:
            self.lobby_nature = LobbyNature.CREATE_LOBBY
            self.lobby_conf = lobby_conf
            category_name = lobby_conf['category_name']

            # global_state.SESSIONS_TO_CAT_ROOM_IDS[host_id] = (self.room_id, category_name)
            global_state.CAT_ROOM_IDS_TO_LOBBIES[category_name][self.room_id] = self

            garbage_collector = threading.Timer(15, destroyUnusedLobby, args=(self.room_id, category_name))
            self.lobby_conf['garbage_collector'] = garbage_collector
            garbage_collector.start()

        print("### in lobby_socket.py ###")
        print('session : room_id #', global_state.SESSIONS_TO_CAT_ROOM_IDS)
        print('cat_room_id : lobby #', global_state.CAT_ROOM_IDS_TO_LOBBIES)

        return res, error