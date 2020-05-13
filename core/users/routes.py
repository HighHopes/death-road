from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import current_user, login_required, login_user, logout_user

from sqlalchemy.exc import IntegrityError

from core import db, bcrypt
from core.models import User
from core.utils.unread_msgs import unread_msgs

from core.users.forms import RegistrationForm, LoginForm, UpdateAccount

users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("users.account_home"))

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")

        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            hidemail=False,
            msg_per_page=5)

        db.session.add(user)
        db.session.commit()

        flash("Your account has been created. You can nou login.", "success")

    return render_template("register.html", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("users.account_home"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)

            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for("users.account_home"))
        else:
            flash('Login Error. Please check Username and Password', "danger")

    return render_template("login.html", form=form)


@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.home"))


@users.route("/account")
@login_required
def account_home():

    # Get the number of unread messages
    get_unread_msgs = unread_msgs(current_user.username)
    return render_template("account_home.html", get_unread_msgs=get_unread_msgs)


@users.route("/account/update", methods=["GET", "POST"])
@login_required
def account_update():
    form = UpdateAccount()

    # Get the number of unread messages
    get_unread_msgs = unread_msgs(current_user.username)

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.hidemail = form.hidemail_checkbox.data
        current_user.msg_per_page = form.msg_per_page.data

        try:
            db.session.commit()
            flash("Your account has been updated.", "success")
            redirect(url_for("users.account_home"))
        except IntegrityError:
            db.session.rollback()

            flash("Username or E-mail already exists.", "danger")
            redirect(url_for("users.account_home"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.hidemail_checkbox.data = current_user.hidemail
        form.msg_per_page.data = current_user.msg_per_page

    return render_template("account_update.html", form=form, get_unread_msgs=get_unread_msgs)


@users.route("/profile/<int:id>")
@login_required
def profile(id):
    user = User.query.get_or_404(id)

    # Get the number of unread messages
    get_unread_msgs = unread_msgs(current_user.username)

    return render_template("profile.html", user=user, get_unread_msgs=get_unread_msgs)
