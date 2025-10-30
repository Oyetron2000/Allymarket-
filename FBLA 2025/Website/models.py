from Website import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    FirstName = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    notes = db.relationship('Note')
    tasks = db.relationship('Task')
    user_type = db.Column(db.String(150), nullable=False)

class Journal(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    title = db.Column(db.String(50))
    note_count = db.column(db.Integer)
    date = db.Column(db.DateTime(timezone = True), default = func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Note(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    title = db.Column(db.String(50))
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone = True), default = func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Task(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    title = db.Column(db.String(50))
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone = True), default = func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.Boolean, default = False)

class Project(db.Model):
    status = db.Column(db.Float, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

