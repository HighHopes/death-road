from flask import Blueprint, render_template
from flask_login import login_required

hero = Blueprint("hero", __name__)


@hero.route("/hero/")
@hero.route("/hero/overview")
@login_required
def hero_home():
    """
    Homepage for hero
    """
    return render_template("hero_home.html")


@hero.route("/hero/training")
@login_required
def hero_training():
    """
    Homepage for hero
    """
    return render_template("hero_training.html")
