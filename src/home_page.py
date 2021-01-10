from flask import render_template, Blueprint, make_response

bp = Blueprint('home_page', __name__)

@bp.route("/")
def home():
    response = make_response(render_template('home.html', name=None))
    return response