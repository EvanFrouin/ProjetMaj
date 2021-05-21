from functools import wraps
from flask import Blueprint, render_template, request, abort
from flask_login import login_required, current_user
from ..db import get_patient_by_query

admin = Blueprint('admin', __name__)


def admin_required(f):
	@login_required
	@wraps(f)
	def route(*args, **kwargs):
		if not current_user.role == "admin":
			abort(403)
		return f(*args, **kwargs)
	return route


@admin.route('/admin/home')
@admin_required
def home():
    return render_template("admin/home.html")

@admin.route('/admin/users')
@admin_required
def users():
	return {'code': 'ok'}


@admin.route('/admin/patients')
@admin_required
def patients():
	return {'code': 'ok'}


@admin.route('/admin/rooms')
@admin_required
def rooms():
	return {'code': 'ok'}
