from flask import (Blueprint, g, make_response, redirect, render_template,
                   request, session, url_for)

from src.helpers import data_integrity

from src.business_logic import definitions, global_state
from src.helpers import common_helpers
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
    lobby = common_helpers.retrieveRoomFromID(room_id)

    if lobby is None:
        if 'return_to_cat' in request.args:
            category_name = request.args['return_to_cat']
            if category_name in definitions.CATEGORY_NAMES:
                return redirect(url_for('sekai.lobbies', category_name=category_name))
        return redirect(url_for('sekai.sekai')) #TODO: flash message missing. Also, maybe we can refactor this if it gets repeated.
    
    lobby_conf = lobby.lobby_conf
    if data_integrity.dictIsCorrupted(['category_name', 'lobby_name', 'host_id'], lobby_conf):
        return "The data was corrupted :c. Please reload the page."
    category_name = lobby_conf['category_name']
    host_id = lobby_conf['host_id']
    lobby_name = lobby_conf['lobby_name']

    is_host = False
    if host_id == g.player_id:
        is_host = True

    category = definitions.CATEGORIES[category_name]
    response = make_response(render_template('lobby.html', player_name=g.player_name,
                                                           category=category,
                                                           lobby_name=lobby_name,
                                                           is_host=is_host))
    return response
