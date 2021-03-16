import threading
import uuid

from src.business_logic import definitions
from src.business_logic import game_definitions
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
host_name
is_private
lobby_password - not atm

garbage_collector

# In lobby (IN_LOBBY) #

host_sid
players_version
players__synchro
slots_synchro
game_settings_synchro

@ players - key = pos

player_id
player_name
player_sid

@ game_settings

version
game_type
difficulty
topic
filters

'''

class Lobby():
    
    def __init__(self):
        self.room_id = str(uuid.uuid4())
        self.lobby_nature = LobbyNature.NONE
        self.lobby_conf = dict()

    def setLobbyNature(self, lobby_nature, lobby_params):
        error = None
        res = None
        if lobby_nature == LobbyNature.CREATE_LOBBY:
            self.lobby_nature = LobbyNature.CREATE_LOBBY
            self.lobby_conf = lobby_params
            category_name = lobby_params['category_name']

            # global_state.SESSIONS_TO_CAT_ROOM_IDS[host_id] = (self.room_id, category_name)
            global_state.CAT_ROOM_IDS_TO_LOBBIES[category_name][self.room_id] = self

            garbage_collector = threading.Timer(15, destroyUnusedLobby, args=(self.room_id, category_name))
            self.lobby_conf['garbage_collector'] = garbage_collector
            garbage_collector.start()
        elif lobby_nature == LobbyNature.IN_LOBBY:
            self.lobby_conf['host_sid'] = lobby_params['player_sid']

            host_player = dict()
            host_player['player_id'] = self.lobby_conf['host_id']
            host_player['player_name'] = self.lobby_conf['host_name']
            host_player['player_sid'] = self.lobby_conf['host_sid']
            players_conf = {0:host_player, 1:None, 2:None, 3:None, 4:None, 5:None, 6:None, 7:None, 8:None, 9:None}
            self.lobby_conf['players'] = players_conf
            self.lobby_conf['players_version'] = 1

            self.lobby_conf['players_synchro'] = list()
            self.lobby_conf['slots_synchro'] = {0:None, 1:None, 2:None, 3:None, 4:None, 5:None, 6:None, 7:None, 8:None, 9:None}
            self.lobby_conf['game_settings_synchro'] = None

            category_name = self.lobby_conf['category_name']
            # It shouldn't be necessary to check if the category_name is correct.
            category = definitions.CATEGORIES[category_name]
            topic = category.topics[0]
            filters = topic.filters
            game_settings = {'version':1,
                             'game_type':game_definitions.GameType.CLASSIC,
                             'difficulty':game_definitions.GameDifficulty.CASUAL,
                             'topic':topic.name,
                             'filters':filters}
            self.lobby_conf['game_settings'] = game_settings
            
            self.lobby_nature = LobbyNature.IN_LOBBY

        print("### in lobby_logic.py ###")
        print('session : room_id #', global_state.SESSIONS_TO_CAT_ROOM_IDS)
        print('cat_room_id : lobby #', global_state.CAT_ROOM_IDS_TO_LOBBIES)

        return res, error