import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__, static_folder='Static', template_folder='Templates')
    app.config['SECRET_KEY'] = '1 luv @ppl3s'
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/uploads/profiles')

    # ✅ Render-safe absolute path for SQLite
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'instance', DB_NAME)
    db_path = os.path.abspath(db_path)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"

    db.init_app(app)

    from .view import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

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
    # ✅ Ensure database file and directory exist before creation
    db_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'instance')
    os.makedirs(db_dir, exist_ok=True)
    with app.app_context():
        db.create_all()
