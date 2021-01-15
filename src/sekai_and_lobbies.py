from flask import Blueprint, render_template, request, make_response

from src.helpers import data_integrity

bp = Blueprint('sekai', __name__, url_prefix="/sekai")

@bp.route("/", methods=("GET", "POST"))
def sekai():
    if request.method == "POST":
        pass
    response = make_response(render_template('sekai.html', name=None))
    return response