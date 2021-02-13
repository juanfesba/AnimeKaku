import uuid

from enum import Enum

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

    def changeRoomNature(self, room_nature):
        if room_nature == RoomNature.CREATE_LOBBY:
            pass

        return