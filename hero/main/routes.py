from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user

from hero import db
from hero.main.forms import SubscriptionForm
from hero.models import Subscription

main = Blueprint("main", __name__)


@main.route("/", methods=["GET", "POST"])
def home():
    if current_user.is_authenticated:
        return redirect(url_for("users.account"))

    form = SubscriptionForm()

    if form.validate_on_submit():
        sub = Subscription(email=form.email.data)
        db.session.add(sub)
        db.session.commit()

        flash("Your email has been successfully registered!", "success")

    return render_template("homepage.html", title="Death Road", form=form)


@main.route("/about")
def about():
    if current_user.is_authenticated:
        return redirect(url_for("users.account"))

    return render_template("about.html", title="About Death Road")
