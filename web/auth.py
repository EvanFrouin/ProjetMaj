from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from .models import User

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template("login.html")


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.objects(email=email).first()

    if not user or password != user.password:
        flash('Wrong credentials, please try again')
        return redirect(url_for('auth.login'))

    login_user(user)
    return redirect(url_for('main.profile'))


@auth.route('/signup')
def signup():
    return render_template("signup.html")


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.objects(name=name).first()

    if user:
        flash('This email address is already in use')
        return redirect(url_for('auth.signup'))

    user = User(email=email, name=name, password=password)
    user.save()

    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
