from flask import Blueprint, render_template
from flask_login import login_required

from core import db
from core.models import User, Hero

stats = Blueprint("stats", __name__)


@stats.route("/statistics")
@login_required
def statistics():
    stats = db.session.query(User, Hero).outerjoin(Hero, User.id == Hero.acc_id)

    return render_template("statistics.html", stats=stats)
