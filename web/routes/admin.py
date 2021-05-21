from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from ..db import get_patient_by_query

admin = Blueprint('admin', __name__)


@admin.route('/admin/home')
@login_required
def home():
    return render_template("admin/home.html")
