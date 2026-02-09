from . import db
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    FirstName = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    notes = db.relationship('Note')
    tasks = db.relationship('Task')
    # was a plain class attribute; keep your default behavior in views instead of relying on this:
    biz_added = False
    user_type = db.Column(db.String(150), nullable=False, default='customer')
    profile_image = db.Column(db.String(150), nullable=True) 

    # NEW: give the user a relationship to their businesses
    businesses = db.relationship(
        'Business',
        backref='owner',
        lazy=True,
        cascade='all, delete-orphan'
    )
    reviews = db.relationship('Review', back_populates='user', cascade='all, delete-orphan')

class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # not unique; different users can choose the same name
    biz_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    image_file = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    location = db.Column(db.String(200))
    biz_phone = db.Column(db.String(150))
    biz_email = db.Column(db.String(150))
    biz_site = db.Column(db.String(200))

   
    reviews = db.relationship('Review', back_populates='business', cascade='all, delete-orphan')
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)

    user = db.relationship('User', back_populates='reviews')
    business = db.relationship('Business', back_populates='reviews')
    


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
