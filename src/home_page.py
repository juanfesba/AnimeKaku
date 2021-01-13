from flask import render_template, Blueprint, make_response, request, flash

bp = Blueprint('home_page', __name__)

@bp.route("/", methods=("GET", "POST"))
def home():
    if request.method == "POST":
        input_player_name = request.form.get('input_player_name') #TODO: make this type of checks with a helper function
        if input_player_name is None:
            return "Did not receive any player name :c"
        return request.form.get('input_player_name')

    response = make_response(render_template('home.html', name=None))
    return response