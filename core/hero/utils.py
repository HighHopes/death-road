from core import db
from core.models import Hero

from datetime import datetime


def acc_has_hero(current_acc_id):
    """
    Checks if there is already a hero created connected to the current account

    :param current_acc_id: gets the current id for the account [current_user.id]
    :return: TRUE if there is already a hero created to the current account, otherwise returns FALSE
    """

    hero = Hero.query.filter_by(acc_id=current_acc_id).first()

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


def hp_regeneration(current_acc_id):
    """
    Checks if HP is lower than HP_max. IF this is true it stores the last check datetime.now(). This is used
    to calculate the HP regenerated over time. At least 5 seconds needs to pass to start the calculations. This
    prevents multiple refresh of the page. It does not update DB if the HP is full.
    This function is added at the start of every page, so the regenerations 'works' every time a page is accesed.

    :param current_acc_id: gets the current id for the account [current_user.id]
    :return: does not return a specific value, but if the HP < HP_max then it updates the current database for the
        hero's HP.
    """

    regen = Hero.query.filter_by(acc_id=current_acc_id).first()

    if regen.alive == 2 and regen.hp < regen.hp_max:
        time_passed = deltatime(datetime.now(), regen.hp_check_regen)

        if time_passed > 4:
            regen.hp += time_passed * regen.hp_regen_rate

            if regen.hp > regen.hp_max:
                regen.hp = regen.hp_max

            regen.hp_check_regen = datetime.now()
            db.session.commit()


def revive_hero(current_acc_id):
    """
    If current status of the hero is Reviving (1) then it calculates the time needed to revive the hero.
    After the Hero is revived, the HP it is set to full.

    Can be set a base value from database or hardcoded. At the moment, for testing purposes it is set for 10 seconds.

    :param current_acc_id:  gets the current id for the account [current_user.id]
    :return:
    """
    revive = Hero.query.filter_by(acc_id=current_acc_id).first()

    time_passed = deltatime(datetime.now(), revive.death_check)

    if time_passed > 9:
        revive.alive = 2
        revive.hp = revive.hp_max
        db.session.commit()