from flask import (Blueprint, g, make_response, redirect, render_template,
                   request, url_for)

from src.business_logic import definitions
from src.helpers import data_integrity
from src.helpers import frontend
from src.session_connection import authentication

bp = Blueprint('sekai', __name__, url_prefix="/sekai")

@bp.before_request
def beforeAppRequest():
    authentication.load_logged_in_user()
    if g.player_name is not None:
        return
    return redirect(url_for('home_page.home'))

@bp.route("/", methods=("GET", "POST"))
def sekai():
    if request.method == "POST":
        pass
    category_names = frontend.fixColumnCount(definitions.category_names, 3)
    response = make_response(render_template('sekai.html',
                                              player_name=g.player_name,
                                              categories=category_names))
    return response

@bp.route("/<category_name>", methods=("GET", "POST"))
def lobbies(category_name=None):
    if category_name is None:
        return "The data was corrupted :c. Please reload the page."
    category_name = str(category_name)
    category_name = category_name.lower()
    if category_name not in definitions.category_names:
        return "The data was corrupted :c. Please reload the page."
    category = definitions.categories[category_name]

    # POST (create_lobby)
    if request.method == "POST":
        if data_integrity.dictIsCorrupted(['input_lobby_name', 'input_choose_topic', 'difficulty_checkbox'], request.form):
            return "The data was corrupted :c. Please reload the page."
        input_lobby_name = str(request.form.get('input_lobby_name'))
        input_choose_topic = str(request.form.get('input_choose_topic'))
        difficulty_checkbox = str(request.form.get('difficulty_checkbox'))

        print(request.form.get('Male_Characters_filter'))
    
    # GET
    response = make_response(render_template('category.html', player_name=g.player_name, category=category))
    return response
