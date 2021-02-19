from flask import (Blueprint, make_response, redirect, render_template,
                   request, session, url_for, g)

from src.helpers import data_integrity
from src.session_connection import authentication

bp = Blueprint('home_page', __name__)

@bp.before_request
def beforeAppRequest():
    authentication.load_logged_in_user()
    if g.player_name is None:
        return
    return redirect(url_for('sekai.sekai'))

@bp.route("/", methods=("GET", "POST"))
def home():
    if request.method == "POST":
        if data_integrity.dictIsCorrupted(['input_player_name'], request.form):
            return "The data was corrupted :c. Please reload the page."
        input_player_name = str(request.form.get('input_player_name'))
        session["player_name"] = input_player_name #TODO: Maybe move to authentication module when necessary.
        session["player_id"] = authentication.generatePlayerID()
        session["room_id"] = None
        session["category_name"] = None
        return redirect(url_for('sekai.sekai'))
    #if request.method == "GET"
    response = make_response(render_template('home.html', name=None))
    return response
