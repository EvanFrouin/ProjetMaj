import csv
from flask_mongoengine import MongoEngine
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
    with open('C:/Users/Utilisateur/Desktop/ProjetMaj/web/db/DB.csv', newline='', encoding='utf-8') as data:
        r = csv.reader(data, delimiter=';')
        next(r, None)
        for row in r:
            insert_patient(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])


def get_user_by_email(email):
    return User.objects(email=email).first()


def insert_user(email, name, password):
    user = User(email=email, name=name, password=password)
    user.save()


def get_patient_by_name(name):
    return Patient.objects(name=name).first()


def insert_patient(name, surname, gender,
                   date_of_birth, place_of_birth, phone_number,
                   size, weight, blood_type, social_number):
    patient = Patient(name=name, surname=surname, gender=gender,
                      date_of_birth=date_of_birth, place_of_birth=place_of_birth, phone_number=phone_number,
                      size=size, weight=weight, blood_type=blood_type, social_number=social_number)
    patient.save()
