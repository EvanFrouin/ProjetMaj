from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from ..db import get_patient_by_query

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


@main.route('/search', methods=['POST'])
@login_required
def patient_query():
	query = request.form.get('query')
	return render_template("search.html", results=get_patient_by_query(gender=query))
