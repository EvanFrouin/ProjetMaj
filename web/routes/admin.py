from functools import wraps
from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
from ..db import get_all_users

admin = Blueprint('admin', __name__)


def admin_required(f):
    @login_required
    @wraps(f)
    def route(*args, **kwargs):
        if not current_user.is_admin:
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
    return render_template("admin/users.html", results=get_all_users())


@admin.route('/admin/rooms')
@admin_required
def rooms():
    return {'code': 'ok'}
