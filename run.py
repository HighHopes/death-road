from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

db.init_app(app)

from main.routes import main

app.register_blueprint(main)

if __name__ == "__main__":
    app.run()
