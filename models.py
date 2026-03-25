from extensions import db
from flask_login import UserMixin

class Parent(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(200))
    is_admin = db.Column(db.Boolean, default=False)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    grade = db.Column(db.String(20))
    dob = db.Column(db.String(20))
    address = db.Column(db.String(200))
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'))

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200))
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'))