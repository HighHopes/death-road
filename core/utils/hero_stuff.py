from core import db
from core.models import Hero, HeroPoints

from datetime import datetime


def acc_has_hero(current_acc_id):
    """
    Checks if there is already a hero_main created connected to the current account

    :param current_acc_id: gets the current id for the account [current_user.id]
    :return: TRUE if there is already a hero_main created to the current account, otherwise returns FALSE
    """

    hero = Hero.query.filter_by(hid=current_acc_id).first()

    return False if hero else True


def deltatime(now, then):
    """
    Calculates the seconds passed from two date times. Used for calculation of HP regeneration

    :param now: the current datetime.now()
    :param then: last datetime storrend in databased.
    :return: seconds passed since last check
    """

    tdelta = now - then

    return tdelta.days * 24 * 3600 + tdelta.seconds


def hp_max(points):
    """
    1 point = 20 HP
    :param points: hp_points
    :return: max hp based on the formula
    """

    return points * 20


def hp_regeneration(current_acc_id):
    """
    Checks if HP is lower than HP_max. IF this is true it stores the last check datetime.now(). This is used
    to calculate the HP regenerated over time. At least 5 seconds needs to pass to start the calculations. This
    prevents multiple refresh of the page. It does not update DB if the HP is full.
    This function is added at the start of every page, so the regenerations 'works' every time a page is accesed.

    :param current_acc_id: gets the current id for the account [current_user.id]
    :return: does not return a specific value, but if the HP < HP_max then it updates the current database for the
        hero_main's HP.
    """

    regen = db.session.query(Hero, HeroPoints).\
        join(HeroPoints, Hero.hid == HeroPoints.hpid).\
        filter(Hero.hid == current_acc_id).\
        first()

    if regen[0].alive == 2 and regen[0].hp < hp_max(regen[1].hp_point):
        time_passed = deltatime(datetime.now(), regen[0].hp_check_regen)

        if time_passed > 0:
            regen[0].hp += time_passed * regen[0].hp_regen_rate

            if regen[0].hp > hp_max(regen[1].hp_point):
                regen[0].hp = hp_max(regen[1].hp_point)

            regen[0].hp_check_regen = datetime.now()
            db.session.commit()


def revive_hero(current_acc_id):
    """
    If current status of the hero_main is Reviving (1) then it calculates the time needed to revive the hero_main.
    After the Hero is revived, the HP it is set to full.

    Can be set a base value from database or hardcoded. At the moment, for testing purposes it is set for 10 seconds.

    :param current_acc_id:  gets the current id for the account [current_user.id]
    :return:
    """

    revive = db.session.query(Hero, HeroPoints).\
        join(HeroPoints, Hero.hid == HeroPoints.hpid).\
        filter(Hero.hid == current_acc_id).\
        first()

    time_passed = deltatime(datetime.now(), revive[0].death_check)

    if time_passed >= revive[0].revive_time:
        revive[0].alive = 2
        revive[0].hp = hp_max(revive[1].hp_point)
        db.session.commit()


def level_up(current_acc_id):
    """
    Calculates when hero_main is leveling up based on the current experience and the next level requirements exp.
    If the hero_main current exp is higher than the max exp then the hero_main levels up with 1 unit and current exp is reseated
    to 0. Next exp is incremented by percentage multiplication based on the previous exp needed.

    :param current_acc_id:  gets the current id for the account [current_user.id]
    :return:
    """

    hero_lvl = Hero.query.filter_by(hid=current_acc_id).first()

    hero_lvl.level += 1
    hero_lvl.level_date = datetime.now()
    hero_lvl.next_lvl_exp = hero_lvl.next_lvl_exp + int(round(hero_lvl.next_lvl_exp * 1.10))

    db.session.commit()


def battle_return_time(current_acc_id):
    hero = Hero.query.filter_by(hid=current_acc_id).first()

    time_passed = deltatime(datetime.now(), hero.return_from_action)

    if time_passed >= hero.return_seconds:
        hero.action = 0
        db.session.commit()