from flask import (Blueprint, g, make_response, redirect, render_template,
                   request, session, url_for)

from src.business_logic import definitions
from src.business_logic import global_state
from src.business_logic import lobby_logic
from src.helpers import frontend
from src.session_connection import authentication

bp = Blueprint('sekai', __name__, url_prefix="/sekai")

@bp.before_request
def beforeAppRequest():
    authentication.load_logged_in_user()
    if g.player_name is None:
        return redirect(url_for('home_page.home'))
    return

@bp.route("/", methods=("GET", "POST"))
def sekai():
    if request.method == "POST":
        pass
    category_names = frontend.fixColumnCount(definitions.CATEGORY_NAMES, 3)
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
    if category_name not in definitions.CATEGORY_NAMES:
        return "The data was corrupted :c. Please reload the page."

    # POST (create_lobby)
    if request.method == "POST":
        if 'input_lobby_name' not in request.form:
            return "The data was corrupted :c. Please reload the page."

        input_lobby_name = str(request.form.get('input_lobby_name'))
        if input_lobby_name == "" or len(input_lobby_name)>20:
            return "The data was corrupted :c. Please reload the page."

        lobby = lobby_logic.Lobby()
        room_id = lobby.room_id
        lobby_nature = lobby_logic.LobbyNature.CREATE_LOBBY
        lobby_params = {'lobby_name' : input_lobby_name,
                      'category_name' : category_name,
                      'host_id' : g.player_id,
                      'host_name' : g.player_name,
                      'is_private' : False,
                      'lobby_password' : None}
        _res, _error = lobby.setLobbyNature(lobby_nature, lobby_params)

        return redirect(url_for('lobby.inLobby', room_id=room_id))

    # GET
    cat_lobbies = global_state.CAT_ROOM_IDS_TO_LOBBIES[category_name].values()
    cat_lobbies = frontend.fixColumnCount(cat_lobbies, 4)
    response = make_response(render_template('category.html', player_name=g.player_name,
                                                              category_name=category_name,
                                                              cat_lobbies=cat_lobbies,
                                                              in_lobby_nature=lobby_logic.LobbyNature.IN_LOBBY))
    return response

    

'''
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
        if input_lobby_name == "":
            return "The data was corrupted :c. Please reload the page."

        input_choose_topic = str(request.form.get('input_choose_topic'))

        difficulty_checkbox = str(request.form.get('difficulty_checkbox'))

        print(request.form.get('Male_Characters_filter'))
    
    # GET
    response = make_response(render_template('category.html', player_name=g.player_name, category=category))
    return response
'''