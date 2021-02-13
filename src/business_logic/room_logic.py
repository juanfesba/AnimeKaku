import threading
import uuid

from src.business_logic import global_state
from src.business_logic import lobby_logic
from enum import Enum

def destroyUnusedRoom(host_id):
    room_id = global_state.SESSIONS_TO_ROOMS_IDS[host_id]
    del global_state.ROOMS_IDS_TO_ROOMS[room_id]

    del global_state.SESSIONS_TO_ROOMS_IDS[host_id] # destroy backwards if it is cancelled in the first del

class RoomNature(Enum):
    NONE = 0
    CREATE_LOBBY = 1
    AFTER_GAME = 2
    IN_LOBBY = 3
    IN_GAME = 4

class Room():
    
    def __init__(self):
        self.id = uuid.uuid4()
        self.room_nature = RoomNature.NONE
        self.room_root = None
        self.room_conf = dict()

    def setRoomNature(self, room_nature, room_conf):
        error = False
        res = None
        if room_nature == RoomNature.CREATE_LOBBY:
            self.room_conf = room_conf
            host_id = room_conf['host_id']

            global_state.ROOMS_IDS_TO_ROOMS[self.id] = self
            global_state.SESSIONS_TO_ROOMS_IDS[host_id] = self.id

            garbage_collector = threading.Timer(10, destroyUnusedRoom, args=(host_id,))
            self.room_conf['garbage_collector'] = garbage_collector
            garbage_collector.start()

        return res, error