import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    # ✅ Explicitly link to your template and static folders
    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Templates'),
        static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Static')
    )

    app.config['SECRET_KEY'] = '1 luv @ppl3s'
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/uploads/profiles')

    # ✅ Absolute path for Render-safe SQLite
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'instance', DB_NAME)
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    db.init_app(app)

    from .view import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Business, Note

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
