from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from sqlalchemy.exc import IntegrityError

from core import db
from core.models import Hero, HeroPoints

from core.hero_main.forms import CreateHeroForm, ReviveHeroForm

from core.utils.hero_stuff import acc_has_hero, hp_max, hp_regeneration, revive_hero, battle_return_time
from core.utils.unread_msgs import unread_msgs

from datetime import datetime, timedelta

hero = Blueprint("hero_main", __name__)


@hero.route("/hero/", methods=["POST", "GET"])
@hero.route("/hero/overview", methods=["POST", "GET"])
@login_required
def hero_home():
    """
    Homepage for hero_main
    """

    # Check if the account has a hero_main created
    # If FALSE redirect user to create a hero_main
    if acc_has_hero(current_user.id):
        return redirect(url_for("hero_main.hero_create"))

    # Get the number of unread messages
    get_unread_msgs = unread_msgs(current_user.username)

    # Get the Hero from DB. Needed for overview page to list Hero details
    hero = db.session.query(Hero, HeroPoints).\
        join(HeroPoints, Hero.hid == HeroPoints.hpid).\
        filter(Hero.hid == current_user.id).\
        first()

    # Check if the hero_main is returning from a battle
    if hero[0].action == 1:
        battle_return_time(current_user.id)

    # Get the Max HP of the hero_main based on HP Points
    max_hp = hp_max(hero[1].hp_point)

    # Regenerate HP of hero_main if it is lower then hp_max
    hp_regeneration(current_user.id)

    # Reviving Hero if it is in state of reviving
    if hero[0].alive == 1:
        revive_hero(current_user.id)

    # Revive and Kill Hero Form
    # Kill hero_main is just for testing purposes
    form = ReviveHeroForm()

    if form.h_kill.data and form.validate_on_submit():
        hero[0].hp = 0
        hero[0].alive = 0
        db.session.commit()

    if form.h_revive.data and form.validate_on_submit():
        hero[0].death_check = datetime.now()
        hero[0].alive = 1
        db.session.commit()

    if form.h_upd_points and form.validate_on_submit():
        pass

    # Time when the hero_main is alive again
    reviving_time = hero[0].death_check + timedelta(seconds=hero[0].revive_time)

    # Time when hero_main will arrive from battle
    returning_time = hero[0].return_from_action + timedelta(seconds=hero[0].return_seconds)

    # Calculates the time when HP will be full
    hp_full_time = hero[0].hp_check_regen + timedelta(seconds=max_hp - hero[0].hp)

    return render_template("hero_home.html", hero=hero, form=form, max_hp=max_hp, hp_full_time=hp_full_time,
                           get_unread_msgs=get_unread_msgs, reviving_time=reviving_time, returning_time=returning_time)


@hero.route("/hero/create", methods=["POST", "GET"])
@login_required
def hero_create():
    """
    If you do not have a hero_main, create one here.
    """

    # Check if the account has a hero_main created
    # If TRUE redirect user to Overview Page
    if not acc_has_hero(current_user.id):
        return redirect(url_for("hero_main.hero_home"))

    form = CreateHeroForm()

    # Get the number of unread messages
    get_unread_msgs = unread_msgs(current_user.username)

    if form.validate_on_submit():
        try:
            hero_main = Hero(
                hid=current_user.id,
                name=form.h_name.data,
                gender=form.h_gender.data,
                date_created=datetime.now(),
                level=1,
                current_exp=0,
                next_lvl_exp=100,
                hp=100,
                hp_regen_rate=1,
                hp_check_regen=datetime.now(),
                alive=2,
                death_check=datetime.now(),
                revive_time=10,
                action=0,
                return_from_action=datetime.now(),
                return_seconds=0)

            hero_points = HeroPoints(
                hpid=current_user.id,
                unused_points=0,
                hp_point=5,
                attack_point=5)

            db.session.add(hero_main)
            db.session.add(hero_points)

            db.session.commit()

            flash("Hero created successfully.", "success")
            return redirect(url_for("hero_main.hero_home"))
        except IntegrityError:
            flash("`" + form.h_name.data + "` already exists. Please choose another name for your hero_main.",
                  "warning")
            return redirect(url_for("hero_main.hero_create"))

    return render_template("hero_create.html", form=form, get_unread_msgs=get_unread_msgs)


@hero.route("/hero/delete")
def hero_delete():
    """
    Delete The current hero_main.
    """

    hero_main = Hero.query.filter_by(hid=current_user.id).first()
    hero_attack_pts = HeroPoints.query.filter_by(hpid=current_user.id).first()

    db.session.delete(hero_main)
    db.session.delete(hero_attack_pts)

    db.session.commit()

    flash("Hero has been deleted.", "danger")
    return redirect(url_for("hero_main.hero_home"))
