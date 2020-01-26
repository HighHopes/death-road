from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from hero.config import Config


db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from hero.main.routes import main
    from hero.users.routes import users

    app.register_blueprint(main)
    app.register_blueprint(users)

    return app
