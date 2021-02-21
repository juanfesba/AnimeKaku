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
    '''if room_id not in cat_lobbies:
        session["lobby_cat"] = None
        return redirect(url_for('sekai.lobbies', category_name=g.lobby_cat)) # pending error (flash) message here'''
    
    return room_id