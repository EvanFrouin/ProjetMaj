from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from ..db import get_all_publishers, get_all_rooms, get_patient_by_query

main = Blueprint('main', __name__)


@main.route('/')
@login_required
def home():
    print(get_all_rooms()[0]["name"])
    print(get_all_publishers()[0]["name"])
    return render_template("dashboard.html", rooms=get_all_rooms(), publishers=get_all_publishers() )


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
    query = request.form.get("query")
    return render_template("search.html", results=get_patient_by_query(name__icontains=query, surname__icontains=query))
