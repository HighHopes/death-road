from hero import db
from flask import Blueprint, render_template
from flask_login import login_required

stats = Blueprint("stats", __name__)

@stats.route("/statistics")
@login_required
def statistics():
    return render_template("statistics.html", title="User statistics")