import os
from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


db = SQLAlchemy()
DB_NAME = "database.db"
def create_app():
    app = Flask(__name__) 
    app.config['SECRET_KEY'] = '1 luv @ppl3s'
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/uploads/profiles')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .view import views
    from .auth import auth

    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')
    
    from .models import User, Note

    create_database(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
        
    return app

def create_database(app):
    with app.app_context():
        db.create_all()
