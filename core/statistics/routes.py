from flask import Blueprint, render_template
from flask_login import login_required, current_user

from core import db
from core.models import User, Hero
from core.utils.unread_msgs import unread_msgs

stats = Blueprint("stats", __name__)


@stats.route("/statistics")
@login_required
def statistics():
    stats = db.session.query(User, Hero).outerjoin(Hero, User.id == Hero.acc_id).order_by(Hero.level.desc())

    # Get the number of unread messages
    get_unread_msgs = unread_msgs(current_user.username)

    return render_template("statistics.html", stats=stats, get_unread_msgs=get_unread_msgs)
