from core import db, login_manager
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Subscription(db.Model):
    """
    Subscription list with emails
    """
    __tablename__ = "subscription"

    id = Column(Integer, primary_key=True)  # email ID
    email = Column(String(120), unique=True, nullable=False)  # email from subscription


class User(db.Model, UserMixin):
    """
    User class for user database
    User profile and account settings goes here
    """
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)  # User ID
    username = Column(String(32), unique=True, nullable=False)  # Username used in registration
    email = Column(String(120), unique=True, nullable=False)  # Email for registration
    password = Column(String(60), nullable=False)  # hashed password
    hidemail = Column(Boolean, nullable=True)  # 0/1 Hide/Show email in public profile
    msg_per_page = Column(Integer, nullable=False)  # get how many messages to show on inbox/outbox page


class Messages(db.Model):
    """
    Message tables for messaging system
    """
    __tablename__ = "messages"

    mid = Column(Integer, primary_key=True)  # message ID
    recipient = Column(String(32))  # recipient - user id from name
    sender = Column(String(32))  # sender - current user id
    subject_msg = Column(String(32))  # subject_msg - msg subject
    body_msg = Column(Text)  # body_msg - message body
    date = Column(DateTime)  # date - date sent
    seen = Column(Boolean)  # seen - message seen
    del_in = Column(Boolean)  # del_in - delete message from inbox
    del_out = Column(Boolean)  # del_out - delete message from outbox


class Hero(db.Model):
    """
    Hero settings. Different settings...
    """

    __tablename__ = "hero"

    acc_id = Column(Integer, primary_key=True)  # hero id connected to account id
    name = Column(String(16), unique=True)  # name of the hero
    gender = Column(Boolean)  # 0 - male / 1 - female
    date_created = Column(DateTime)  # date created the hero
    level = Column(Integer)  # current level of the hero
    current_exp = Column(Integer)  # current experience of hero
    next_lvl_exp = Column(Integer)  # exp needed for next level
    hp = Column(Integer)  # current hero health HP
    hp_max = Column(Integer)  # current hero health HP
    hp_regen_rate = Column(Integer)  # hp regeneration per second
    hp_check_regen = Column(DateTime)  # used to calculate the regenerated hp over time
    alive = Column(Integer)  # Check if hero is Death (0), Reviving (1), Alive (2)
    death_check = Column(DateTime)  # Time when the hero was revived
    attack_point = Column(Integer)  # attack points needed to calculate damage
