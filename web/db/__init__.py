import csv
import os.path
from flask_mongoengine import MongoEngine
from mongoengine.queryset.visitor import Q
from flask_login import UserMixin

db = MongoEngine()


class User(UserMixin, db.Document):
    email = db.StringField()
    name = db.StringField()
    password = db.StringField()


class Patient(db.Document):
    name = db.StringField()
    surname = db.StringField()
    gender = db.StringField()
    date_of_birth = db.StringField()
    place_of_birth = db.StringField()
    phone_number = db.StringField()
    size = db.StringField()
    weight = db.StringField()
    blood_type = db.StringField()
    social_number = db.StringField()


class Room(db.Document):
    name = db.StringField()
    publishers = db.ListField()
    patient = db.ObjectIdField()


def init_patients():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'DB.csv'), newline="", encoding='utf-8') as data:
        r = csv.reader(data, delimiter=';')
        next(r, None)
        for row in r:
            insert_patient(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])


def get_user_by_email(email):
    return User.objects(email=email).first()


def insert_user(email, name, password):
    user = User(email=email, name=name, password=password)
    user.save()


def get_patient_by_query(first=False, **kwargs):
    patients = Patient.objects(
		Q(**{f"{list(kwargs.items())[0][0]}": f"{list(kwargs.items())[0][1]}"}) |
		Q(**{f"{list(kwargs.items())[1][0]}": f"{list(kwargs.items())[1][1]}"})
	)
    if first:
        return patients.first()
    else:
        return patients


def insert_patient(name, surname, gender,
                   date_of_birth, place_of_birth, phone_number,
                   size, weight, blood_type, social_number):
    patient = Patient(name=name, surname=surname, gender=gender,
                      date_of_birth=date_of_birth, place_of_birth=place_of_birth, phone_number=phone_number,
                      size=size, weight=weight, blood_type=blood_type, social_number=social_number)
    patient.save()
