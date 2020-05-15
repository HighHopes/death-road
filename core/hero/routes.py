from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from sqlalchemy.exc import IntegrityError

from core import db
from core.models import Hero, AnimalsTraining

from core.hero.forms import CreateHeroForm, ReviveHeroForm
from core.hero.utils import acc_has_hero, hp_regeneration, revive_hero

from core.utils.unread_msgs import unread_msgs

from datetime import datetime, timedelta
from random import randint

hero = Blueprint("hero", __name__)


@hero.route("/hero/", methods=["POST", "GET"])
@hero.route("/hero/overview", methods=["POST", "GET"])
@login_required
def hero_home():
    """
    Homepage for hero
    """

    # Check if the account has a hero created
    # If FALSE redirect user to create a hero
    if acc_has_hero(current_user.id):
        return redirect(url_for("hero.hero_create"))

    # Get the number of unread messages
    get_unread_msgs = unread_msgs(current_user.username)

    # Get the Hero from DB. Needed for overview page to list Hero details
    hero = Hero.query.filter_by(acc_id=current_user.id).first()

    # Regenerate HP of hero if it is lower then hp_max
    hp_regeneration(current_user.id)

    # Reviving Hero if it is in state of reviving
    if hero.alive == 1:
        revive_hero(current_user.id)

    # Revive and Kill Hero Form
    # Kill hero is just for testing purposes
    form = ReviveHeroForm()

    if form.h_kill.data and form.validate_on_submit():
        hero.hp = 0
        hero.alive = 0
        db.session.commit()

    if form.h_revive.data and form.validate_on_submit():
        hero.death_check = datetime.now()
        hero.alive = 1
        db.session.commit()

    # Time when the hero is alive again
    reviving_time = hero.death_check + timedelta(seconds=hero.revive_time)

    return render_template("hero_home.html", hero=hero, form=form, get_unread_msgs=get_unread_msgs,
                           reviving_time=reviving_time)


@hero.route("/hero/create", methods=["POST", "GET"])
@login_required
def hero_create():
    """
    If you do not have a hero, create one here.
    """

    # Check if the account has a hero created
    # If TRUE redirect user to Overview Page
    if not acc_has_hero(current_user.id):
        return redirect(url_for("hero.hero_home"))

    form = CreateHeroForm()

    # Get the number of unread messages
    get_unread_msgs = unread_msgs(current_user.username)

    if form.validate_on_submit():
        try:
            hero_obj = Hero(
                acc_id=current_user.id,
                name=form.h_name.data,
                gender=form.h_gender.data,
                date_created=datetime.now(),
                level=1,
                current_exp=0,
                next_lvl_exp=100,
                hp=100,
                hp_max=100,
                hp_regen_rate=1,
                hp_check_regen=datetime.now(),
                alive=2,
                death_check=datetime.now(),
                revive_time=10,
                attack_point=5)

            db.session.add(hero_obj)
            db.session.commit()

            flash("Hero created successfully.", "success")
            return redirect(url_for("hero.hero_home"))
        except IntegrityError:
            flash("`" + form.h_name.data + "` already exists. Please choose another name for your hero.", "warning")
            return redirect(url_for("hero.hero_create"))

    return render_template("hero_create.html", form=form, get_unread_msgs=get_unread_msgs)


@hero.route("/hero/delete")
def hero_delete():
    """
    Delete The current hero.
    """

    hid = Hero.query.filter_by(acc_id=current_user.id).first()
    db.session.delete(hid)
    db.session.commit()

    flash("Hero has been deleted.", "danger")
    return redirect(url_for("hero.hero_home"))


@hero.route("/hero/training")
@login_required
def hero_training():
    """
    Training zone for hero
    """

    # Check if the account has a hero created
    # If FALSE redirect user to create a hero
    if acc_has_hero(current_user.id):
        return redirect(url_for("hero.hero_create"))

    # Get the number of unread messages
    get_unread_msgs = unread_msgs(current_user.username)

    # Regenerate HP of hero if it is lower then hp_max
    hp_regeneration(current_user.id)

    # Get the Hero from DB. Needed for stats page to list Hero hero vital infos
    hero = Hero.query.filter_by(acc_id=current_user.id).first()

    # Reviving Hero if it is in state of reviving
    if hero.alive == 1:
        revive_hero(current_user.id)

    # Time when the hero is alive again
    reviving_time = hero.death_check + timedelta(seconds=hero.revive_time)

    return render_template("hero_training.html", hero=hero, get_unread_msgs=get_unread_msgs,
                           reviving_time=reviving_time)


@hero.route("/hero/training/lvl_<int:id>")
@login_required
def train(id):
    """
    Training on different levels for different animals
    """

    # Check if the account has a hero created
    # If FALSE redirect user to create a hero
    if acc_has_hero(current_user.id):
        return redirect(url_for("hero.hero_create"))

    # Get the number of unread messages
    get_unread_msgs = unread_msgs(current_user.username)

    # Get the Hero from DB. Needed for stats page to list Hero hero vital infos
    hero = Hero.query.filter_by(acc_id=current_user.id).first()

    if hero.hp == 0:
        return redirect(url_for("hero.hero_home"))

    # Get the animal for the current training level
    animal = AnimalsTraining.query.get_or_404(id)

    # The Process of fighting - 1st try
    # __________________________________________________ #

    output = []  # output messages

    # Creating variables for the fight
    hero_hp = hero.hp
    animal_hp = animal.hp

    while True:
        hero_dmg = randint(round(hero.attack_point * 0.5), round(hero.attack_point * 1.25))

        animal_hp -= hero_dmg
        if animal_hp <= 0:
            out = "The Hero hit The Animal with " + str(hero_dmg) + " dmg. The Animal is DEAD. Hero WON this battle."
            output.append(out)

            break
        else:
            out = "Hero hit the Animal with " + str(hero_dmg) + ". Animal HP is " + str(animal_hp)
            output.append(out)

        animal_dmg = randint(round(animal.attack_point * 0.5), round(animal.attack_point * 1.25))
        hero_hp -= animal_dmg
        if hero_hp <= 0:
            out = "The Animal hit the Hero with " + str(animal_dmg) + " dmg. Hero is DEAD. The Animal won this battle."
            output.append(out)

            break
        else:
            out = "Animal hit the Hero with " + str(animal_dmg) + ". Hero HP is " + str(hero_hp)
            output.append(out)

    if hero_hp <= 0:
        hero.hp = 0
        hero.alive = 0
    else:
        hero.hp_check_regen = datetime.now()
        hero.hp = hero_hp
        hero.current_exp += animal.exp_given

    db.session.commit()

    return render_template("hero_train.html", animal=animal, hero=hero, get_unread_msgs=get_unread_msgs, output=output)
