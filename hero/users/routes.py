from hero import db, bcrypt
from flask import Blueprint, render_template, flash
from hero.users.forms import RegistrationForm
from hero.models import User

users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)

        db.session.add(user)
        db.session.commit()

        flash("Your account has been created. You can nou login.", "success")

    return render_template("register.html", title="Register", form=form)
