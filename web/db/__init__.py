import csv
import os.path
from functools import reduce

from flask_mongoengine import MongoEngine
from mongoengine.queryset.visitor import Q
from flask_login import UserMixin

db = MongoEngine()


class User(UserMixin, db.Document):
    email = db.StringField()
    name = db.StringField()
    password = db.StringField()
    is_admin = db.BooleanField()


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


def parse_params(param):
    return ({key: param[key]} for key in param)


def build_Q(parameters):
    return (Q(**param) for param in parse_params(parameters))


def build_query(parameters):
    return reduce(lambda a, b: a | b, build_Q(parameters))


def reset_patient_collection():
    Patient.drop_collection()
    init_patients()


def init_patients():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'DB.csv'), newline="", encoding='utf-8') as data:
        r = csv.reader(data, delimiter=';')
        next(r, None)
        for row in r:
            insert_patient(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])


def get_all_users():
    return User.objects


def get_user_by_email(email):
    return User.objects(email=email).first()


def insert_user(email, name, password):
    user = User(email=email, name=name, password=password, isAdmin=False)
    user.save()


def delete_user(user_id):
    User.objects(id=user_id).first().delete()


def update_user_role(user_id):
    role = (User.objects(id=user_id).first()).is_admin
    User.objects(id=user_id).update_one(set__is_admin=not role)


def get_patient_by_query(first=False, **kwargs):
    patients = Patient.objects(build_query(kwargs))
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


def delete_patient(patient_id):
    Patient.objects(id=patient_id).first().delete()


def update_patient(patient_id, data):
    Patient.objects(id=patient_id).update_one(**data)
