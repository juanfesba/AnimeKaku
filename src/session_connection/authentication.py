from flask import g, session

player_id_gen = "0"

def load_logged_in_user():
    player_name = session.get("player_name")
    player_id = session.get("player_id")

    if player_name is None:
        g.player_name = None
    else:
        g.player_name = player_name

    if player_id is None:
        g.player_id = 0

def generatePlayerID():
    global player_id_gen
    generated_id = str(player_id_gen)
    player_id_gen += 1
    return generated_id