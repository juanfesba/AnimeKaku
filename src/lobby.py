from flask import Blueprint, g, redirect, url_for

from src.session_connection import authentication

bp = Blueprint('lobby', __name__, url_prefix="/lobby")

@bp.before_request
def beforeAppRequest():
    authentication.load_logged_in_user()
    if g.player_name is not None:
        return
    return redirect(url_for('home_page.home'))

@bp.route("/<room_id>", methods=("GET", "POST"))
def in_lobby(room_id=None):
    return room_id