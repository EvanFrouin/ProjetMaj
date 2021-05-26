from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user
from ..db import get_user_by_email, insert_user

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
        flash("Mauvais email ou mot de passe. Veuillez réessayer.")
        return redirect(url_for('auth.login'))

    login_user(user)
    return redirect(url_for('main.home'))


@auth.route('/signup')
def signup():
    return render_template("auth/signup.html")


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('username')
    password = request.form.get('password')

    try:
        user = get_user_by_email(email)
    except:
        print("no users in the DB")
        
    if user:
        flash("Cette adresse email est déjà utilisée.")
        return redirect(url_for('auth.signup'))

    insert_user(email, name, password)

    flash("Compte créé avec succès !")
    return redirect(url_for('auth.login'))


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
