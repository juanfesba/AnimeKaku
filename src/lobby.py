from flask import Blueprint, g, redirect, request, session, url_for

from src.business_logic import definitions
from src.business_logic import global_state
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
            if category_name not in definitions.CATEGORY_NAMES:
                return redirect(url_for('sekai.sekai'))
            return redirect(url_for('sekai.lobbies', category_name=category_name))
        return redirect(url_for('sekai.sekai')) #TODO: flash message missing. Also, maybe we can refactor this if it gets repeated.
    
    return room_id