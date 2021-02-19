from flask import Blueprint, g, redirect, url_for

from src.session_connection import authentication

bp = Blueprint('lobby', __name__, url_prefix="/lobby")

@bp.before_request
def beforeAppRequest():
    authentication.load_logged_in_user()
    if g.player_name is None:
        return redirect(url_for('home_page.home'))
    if g.room_id is None:
        return redirect(url_for('sekai.sekai'))
    return

@bp.route("/<room_id>", methods=("GET", "POST"))
def in_lobby(room_id=None):
    if g.room_id != room_id:
        return redirect(url_for('lobby.in_lobby', room_id=g.room_id))

    return room_id