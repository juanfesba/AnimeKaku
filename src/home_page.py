from flask import render_template, Blueprint

bp = Blueprint('home_page', __name__)

@bp.route("/")
def home():
    return render_template("home.html", name=None)