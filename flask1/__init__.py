from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask1.config import Config
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt_ = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app(config_file =  Config):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config_file)
    db.init_app(app)
    bcrypt_.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from .auth import auth
        from .blog import blog
        app.register_blueprint(auth)
        app.register_blueprint(blog)
        return app