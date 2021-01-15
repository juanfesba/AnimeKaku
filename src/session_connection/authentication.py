from flask import g, session

def load_logged_in_user():
    player_name = session.get("player_name")

    if player_name is None:
        g.player_name = None
    else:
        g.player_name = player_name