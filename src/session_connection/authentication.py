import uuid

from flask import g, session

def load_logged_in_user():
    player_name = session.get("player_name")
    player_id = session.get("player_id")
    room_id = session.get("room_id")
    category_name = session.get("category_name")

    if player_name is None:
        g.player_name = None
    else:
        g.player_name = player_name

    if player_id is None:
        g.player_id = None
    else:
        g.player_id = player_id

    if room_id is None:
        g.room_id = None
    else:
        g.room_id = room_id

    if category_name is None:
        g.category_name = None
    else:
        g.category_name = category_name

def generatePlayerID():
    return str(uuid.uuid4())