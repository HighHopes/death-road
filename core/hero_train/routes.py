from flask import Blueprint, render_template, redirect, url_for, flash, Markup
from flask_login import login_required, current_user

from core import db
from core.models import Hero, HeroPoints, AnimalsTraining
from core.utils.hero_stuff import acc_has_hero, hp_regeneration, hp_max, battle_return_time, level_up, revive_hero
from core.utils.unread_msgs import unread_msgs

from datetime import timedelta, datetime
from random import randint

training = Blueprint("hero_train", __name__)


@training.route("/hero/training")
@login_required
def hero_training():
    """
    Training zone for hero_main
    """

    # Check if the account has a hero_main created
    # If FALSE redirect user to create a hero_main
    if acc_has_hero(current_user.id):
        return redirect(url_for("hero_main.hero_create"))

    # Get the number of unread messages
    get_unread_msgs = unread_msgs(current_user.username)

    # Regenerate HP of hero_main if it is lower then hp_max
    hp_regeneration(current_user.id)

    # Get the Hero from DB. Needed for stats page to list Hero hero_main vital info
    hero = db.session.query(Hero, HeroPoints).\
        join(HeroPoints, Hero.hid == HeroPoints.hpid).\
        filter(Hero.hid == current_user.id).\
        first()

    # Get the Max HP of the hero_main based on HP Points
    max_hp = hp_max(hero[1].hp_point)

    # Calculates the time when HP will be full
    hp_full_time = hero[0].hp_check_regen + timedelta(seconds=max_hp - hero[0].hp)

    # Check if the hero_main is returning from a battle
    if hero[0].action == 1:
        battle_return_time(current_user.id)

    # Check for level Up
    if hero[0].current_exp >= hero[0].next_lvl_exp:
        level_up(current_user.id)

    # Get all animals for the training section
    animals = AnimalsTraining.query.all()

    # Reviving Hero if it is in state of reviving
    if hero[0].alive == 1:
        revive_hero(current_user.id)

    # Time when the hero_main is alive again
    reviving_time = hero[0].death_check + timedelta(seconds=hero[0].revive_time)

    # Time when hero_main will arrive from battle
    returning_time = hero[0].return_from_action + timedelta(seconds=hero[0].return_seconds)

    return render_template("hero_training.html", hero=hero, animals=animals, hp_full_time=hp_full_time,
                           get_unread_msgs=get_unread_msgs, max_hp=max_hp, reviving_time=reviving_time,
                           returning_time=returning_time)


@training.route("/hero/training/lvl_<int:id>")
@login_required
def train(id):
    """
    Training on different levels for different animals
    """

    # Check if the account has a hero_main created
    # If FALSE redirect user to create a hero_main
    if acc_has_hero(current_user.id):
        return redirect(url_for("hero_main.hero_create"))

    # Get the number of unread messages
    get_unread_msgs = unread_msgs(current_user.username)

    # Get the Hero from DB. Needed for stats page to list Hero hero_main vital info
    hero = db.session.query(Hero, HeroPoints).\
        join(HeroPoints, Hero.hid == HeroPoints.hpid).\
        filter(Hero.hid == current_user.id).\
        first()

    # Get the Max HP of the hero_main based on HP Points
    max_hp = hp_max(hero[1].hp_point)

    # if the user enters the link manual, check if the hp is >0 or redirect user home
    if hero[0].hp == 0:
        return redirect(url_for("hero_main.hero_home"))

    # Check for level Up
    if hero[0].current_exp >= hero[0].next_lvl_exp:
        level_up(current_user.id)

    # Check if the hero_main is returning from a battle
    if hero[0].action == 1:
        battle_return_time(current_user.id)

    # Return message if the hero_main is on it's way to somewhere
    if hero[0].action == 1:
        msg = hero[0].name + " is currently returning from a battle. Wait until your hero_main is home and try again!"
        flash(msg, "warning")
        return redirect(url_for("hero_main.hero_home"))

    # Get the animal for the current training level
    animal = AnimalsTraining.query.get_or_404(id)

    # ----- The Process of fighting - 1st try ----- #

    output = []  # output messages

    # Creating variables for the fight
    hero_hp = hero[0].hp
    animal_hp = animal.hp

    while True:
        hero_dmg = randint(round(hero[1].attack_point * 0.5), round(hero[1].attack_point * 1.26))

        animal_hp -= hero_dmg
        if animal_hp <= 0:
            # IF the hero_main wins the battle
            out = hero[0].name + " hit " + animal.name + " with " + str(hero_dmg) + " dmg. " + animal.name + \
                  "  is DEAD. " + hero[0].name + " WON this battle."
            output.append(out)

            # random experience gained from battle based on the value from db
            exp = randint(round(animal.exp_given * 0.76), round(animal.exp_given * 1.26))

            break
        else:
            out = hero[0].name + " hit " + animal.name + " with " + str(hero_dmg) + ". " + animal.name + \
                  " HP is lowered from " + str(animal_hp + hero_dmg) + " to " + str(animal_hp)
            output.append(out)

        animal_dmg = randint(round(animal.attack_point * 0.5), round(animal.attack_point * 1.26))

        hero_hp -= animal_dmg
        if hero_hp <= 0:
            # IF the animal wins the battle
            out = animal.name + " hit " + hero[0].name + " with " + str(animal_dmg) + " dmg. " + hero[0].name + \
                  " is DEAD. " + animal.name + " won this battle."
            output.append(out)

            # if hero_main is dead 0 exp will gain from battle
            exp = 0

            msg_dead = Markup("<i class='far fa-sad-tear'></i> You have died. Revive your hero and try again!")
            flash(msg_dead, "danger")

            break
        else:
            out = animal.name + " hit " + hero[0].name + " with " + str(animal_dmg) + \
                  ". " + hero[0].name + " HP is lowered from " + str(hero_hp + animal_dmg) + " to " + str(hero_hp)
            output.append(out)

    if hero_hp <= 0:
        hero[0].hp = 0
        hero[0].alive = 0
    else:
        hero[0].hp_check_regen = datetime.now()
        hero[0].action = 1
        hero[0].return_from_action = datetime.now()
        hero[0].return_seconds = animal.duration
        hero[0].hp = hero_hp
        hero[0].current_exp += exp

        # Check for level Up
        if hero[0].current_exp >= hero[0].next_lvl_exp:
            level_up(current_user.id)
            msg_lvl_up = "Congratulation, " + hero[0].name + "! You have leveled up!"
            flash(msg_lvl_up, "success")

    db.session.commit()

    # ----- The Battle is Over ----- #

    # Time when hero_main will arrive from battle
    returning_time = hero[0].return_from_action + timedelta(seconds=hero[0].return_seconds)

    # Calculates the time when HP will be full
    hp_full_time = hero[0].hp_check_regen + timedelta(seconds=max_hp - hero[0].hp)

    return render_template("hero_train.html", animal=animal, hero=hero, max_hp=max_hp, hp_full_time=hp_full_time,
                           get_unread_msgs=get_unread_msgs, output=output, exp=exp, returning_time=returning_time)
