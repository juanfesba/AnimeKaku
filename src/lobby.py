from flask import Blueprint, g, redirect, session, url_for

from src.business_logic import global_state
from src.session_connection import authentication

bp = Blueprint('lobby', __name__, url_prefix="/lobby")

@bp.before_request
def beforeAppRequest():
    authentication.load_logged_in_user()
    if g.player_name is None:
        return redirect(url_for('home_page.home'))
    return

@bp.route("/<room_id>", methods=("GET", "POST"))
def inLobby(room_id=None):
    if g.lobby_cat is None:
        return redirect(url_for('sekai.sekai'))
    if g.lobby_cat not in global_state.CAT_ROOM_IDS_TO_LOBBIES:
        session["lobby_cat"] = None
        return redirect(url_for('sekai.sekai'))
    cat_lobbies = global_state.CAT_ROOM_IDS_TO_LOBBIES[g.lobby_cat]
    if room_id not in cat_lobbies:
        session["lobby_cat"] = None
        return redirect(url_for('sekai.lobbies', category_name=g.lobby_cat)) # pending error (flash) message here
    
    return room_id

@bp.route("/inv/<lobby_cat>/<room_id>", methods=("GET", "POST"))
def inviteLobby(lobby_cat=None, room_id=None):
    if lobby_cat is None or room_id is None:
        return "The data was corrupted :c. Please reload the page."
    session["lobby_cat"] = lobby_cat
    return redirect(url_for('lobby.inLobby', room_id=room_id))