from flask import Blueprint, render_template
from flask_login import current_user
from core.utils.unread_msgs import unread_msgs


errors = Blueprint("errors", __name__)


@errors.app_errorhandler(404)
def error_404(error):
    # Get the number of unread messages
    get_unread_msgs = unread_msgs(current_user.username)

    return render_template("errors/404.html", get_unread_msgs=get_unread_msgs), 404
