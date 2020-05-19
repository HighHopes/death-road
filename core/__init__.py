from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from core.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from core.main.routes import main
    from core.users.routes import users
    from core.statistics.routes import stats
    from core.errors.handlers import errors
    from core.messages.routes import msgs
    from core.hero_main.routes import hero
    from core.hero_train.routes import training

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(stats)
    app.register_blueprint(errors)
    app.register_blueprint(msgs)
    app.register_blueprint(hero)
    app.register_blueprint(training)

    return app
