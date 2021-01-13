from flask import render_template, Blueprint, make_response, request, flash, session, redirect, url_for

bp = Blueprint('home_page', __name__)

@bp.route("/", methods=("GET", "POST"))
def home():
    if request.method == "POST":
        input_player_name = request.form.get('input_player_name') #TODO: make this type of checks with a helper function
        if input_player_name is None:
            return "Did not receive any player name :c"
        session["user_id"] = input_player_name
        return redirect(url_for('home_page.home'))
    response = make_response(render_template('home.html', name=None))
    return response