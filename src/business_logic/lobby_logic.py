import threading
import uuid

from src.business_logic import global_state
from src.business_logic import lobby_logic
from enum import Enum

def destroyUnusedLobby(host_id):
    room_id, category_name = global_state.SESSIONS_TO_CAT_ROOM_IDS[host_id]
    if category_name in global_state.CAT_ROOM_IDS_TO_LOBBIES:
        rooms_in_category = global_state.CAT_ROOM_IDS_TO_LOBBIES[category_name]
        if room_id in rooms_in_category:
            del rooms_in_category[room_id]

    del global_state.SESSIONS_TO_CAT_ROOM_IDS[host_id] # destroy backwards if it is cancelled in the first del

class LobbyNature(Enum):
    NONE = 0
    CREATE_LOBBY = 1
    AFTER_GAME = 2
    IN_LOBBY = 3
    IN_GAME = 4

'''
### lobby_conf

lobby_name
category_name
host_id

garbage_collector

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
            self.lobby_conf = lobby_conf
            host_id = lobby_conf['host_id']
            category_name = lobby_conf['category_name']

            global_state.SESSIONS_TO_CAT_ROOM_IDS[host_id] = (self.room_id, category_name)
            global_state.CAT_ROOM_IDS_TO_LOBBIES[category_name][self.room_id] = self

            garbage_collector = threading.Timer(15, destroyUnusedLobby, args=(host_id,))
            self.lobby_conf['garbage_collector'] = garbage_collector
            garbage_collector.start()
        print('session : room_id #', global_state.SESSIONS_TO_CAT_ROOM_IDS)
        print('cat_room_id : lobby #', global_state.CAT_ROOM_IDS_TO_LOBBIES)

        return res, error