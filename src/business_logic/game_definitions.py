from enum import Enum

class GameType(Enum):
    NONE = 0
    CLASSIC = 1

class GameDifficulty(Enum):
    NONE = 0
    CASUAL = 1
    EXTREME = 2
    
SERIALIZE_GAME_DEFINITIONS = {GameType.NONE : None, GameType.CLASSIC : 'Classic'}
SERIALIZE_GAME_DIFFICULTY = {GameDifficulty.NONE : None, GameDifficulty.CASUAL : 'Casual', GameDifficulty.EXTREME : 'Extreme'}