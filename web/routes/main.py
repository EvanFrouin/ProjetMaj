from flask import Blueprint, render_template
from flask_login import login_required, current_user

main = Blueprint('main', __name__)


@main.route('/')
@login_required
def dashboard():
    return render_template("dashboard.html")


@main.route('/profile')
@login_required
def profile():
    return render_template("profile.html", name=current_user.name)


@main.route('/search')
@login_required
def search():
    return render_template("search.html")
