from flask import Blueprint, render_template, request, make_response, url_for, g, redirect

from src.helpers import data_integrity
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
    response = make_response(render_template('sekai.html', name=None))
    return response