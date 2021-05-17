from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from ..db import User, get_user_by_email, insert_user

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template("auth/login.html")


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    user = get_user_by_email(email)

    if not user or password != user.password:
        flash('Wrong credentials, please try again')
        return redirect(url_for('auth.login'))

    login_user(user)
    return redirect(url_for('main.dashboard'))


@auth.route('/signup')
def signup():
    return render_template("auth/signup.html")


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('username')
    password = request.form.get('password')

    user = get_user_by_email(email)

    if user:
        flash('This email address is already in use')
        return redirect(url_for('auth.signup'))

    insert_user(email, name, password)

    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
