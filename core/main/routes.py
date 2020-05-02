from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user

from core import db
from core.main.forms import SubscriptionForm
from core.models import Subscription

main = Blueprint("main", __name__)


@main.route("/", methods=["GET", "POST"])
def home():
    if current_user.is_authenticated:
        return redirect(url_for("users.account_home"))

    form = SubscriptionForm()

    if form.validate_on_submit():
        sub = Subscription(email=form.email.data)
        db.session.add(sub)
        db.session.commit()

        flash("Your email has been successfully registered!", "success")

    return render_template("homepage.html", form=form)


@main.route("/about")
def about():
    if current_user.is_authenticated:
        return redirect(url_for("users.account_home"))

    return render_template("about.html")
