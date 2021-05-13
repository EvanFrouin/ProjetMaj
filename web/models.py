from flask_login import UserMixin
from . import db


class User(UserMixin, db.Document):
    email = db.StringField()
    name = db.StringField()
    password = db.StringField()
