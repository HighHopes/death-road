from flask import Blueprint, render_template
from flask_login import login_required

from core.models import User

stats = Blueprint("stats", __name__)


@stats.route("/statistics")
@login_required
def statistics():
    all_users = User.query.all()

    return render_template("statistics.html", all_users=all_users)
