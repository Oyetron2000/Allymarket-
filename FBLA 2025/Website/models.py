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
    biz_added = False
    user_type = db.Column(db.String(150), nullable=False, default ='customer') 
    

class Business(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    biz_name = db.Column(db.String(100), unique=True, nullable = False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(100), nullable = False)


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




