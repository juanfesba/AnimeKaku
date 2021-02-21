import uuid

from flask import g, session

def load_logged_in_user():
    player_name = session.get("player_name")
    player_id = session.get("player_id")

    if player_name is None:
        g.player_name = None
    else:
        g.player_name = player_name

    if player_id is None:
        g.player_id = None
    else:
        g.player_id = player_id

def generatePlayerID():
    return str(uuid.uuid4())