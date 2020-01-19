from flask import Flask
from hero.config import Config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from hero.main.routes import main

    app.register_blueprint(main)

    return app
