from hero import db, bcrypt
from flask import Blueprint, render_template, flash, request, redirect, url_for
from hero.users.forms import RegistrationForm, LoginForm, UpdateAccount
from hero.models import User
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy.exc import IntegrityError

users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("users.account"))

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, hidemail=0)

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
    form = UpdateAccount()

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.hidemail = form.hidemail_checkbox.data

        try:
            db.session.commit()
            flash("Your account has been updated.", "success")
            redirect(url_for("users.account"))
        except IntegrityError:
            db.session.rollback()

            flash("Username or E-mail already exists.", "danger")
            redirect(url_for("users.account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.hidemail_checkbox.data = current_user.hidemail

    return render_template("account.html", title="Account", form=form)


@users.route("/profile/<int:id>")
@login_required
def profile(id):
    user = User.query.get_or_404(id)
    return render_template("profile.html", title="User Profile", user=user)
