from hero import db, bcrypt
from flask import Blueprint, render_template, flash, request, redirect, url_for
from hero.users.forms import RegistrationForm, LoginForm
from hero.models import User
from flask_login import current_user, login_required, login_user, logout_user

users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("users.account"))

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)

        db.session.add(user)
        db.session.commit()

        flash("Your account has been created. You can nou login.", "success")

    return render_template("register.html", title="Register", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("users.account"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)

            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for("users.account"))
        else:
            flash('Login Error. Please check Username and Password', "danger")

    return render_template("login.html", title="Login", form=form)


@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.home"))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    return render_template("account.html", title="Account")


@users.route("/profile/<string:user>")
@login_required
def profile(user):
    user = User.query.get_or_404(user)
    return render_template("profile.html", title="User Profile", user=user)
