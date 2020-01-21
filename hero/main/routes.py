from flask import Blueprint, render_template
from hero.main.forms import SubscriptionForm
from hero.models import Subscription

main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def home():
    form = SubscriptionForm()

    if form.validate_on_submit():
        sub = Subscription(email=form.email.data)
        db.session.add(sub)
        db.session.commit()

    return render_template("homepage.html", title="Death Road", form=form)

@main.route("/about")
def about():
    return render_template("about.html", title="About Death Road")
