from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user

from core import db
from core.models import Messages, User
from core.messages.forms import SendMessageForm, DeleteSingleMessageButton, MessageMultipleDelete
from core.utils.unread_msgs import unread_msgs

from datetime import datetime

msgs = Blueprint("msgs", __name__)


@msgs.route("/msg_inbox", methods=["POST", "GET"])
@login_required
def msg_inbox():
    """
    Get messages for INBOX page. Show only messages where recipient is the current logged in user
    """

    # Get Inbox Messages and Paginate them
    page = request.args.get("page", 1, type=int)
    msg_per_page = User.query.get_or_404(current_user.id)

    # Get the number of unread messages
    get_unread_msgs = unread_msgs(current_user.username)

    if request.args and request.args.get("unread") == "true":
        unread_msg_count = Messages.query. \
            filter_by(recipient=current_user.username, del_in=False, seen=False). \
            count()

        msgs_received = Messages.query. \
            order_by(Messages.date.desc()). \
            filter_by(recipient=current_user.username, del_in=False, seen=False). \
            paginate(page=page, per_page=unread_msg_count)
    else:
        msgs_received = Messages.query. \
            order_by(Messages.date.desc()). \
            filter_by(recipient=current_user.username, del_in=False). \
            paginate(page=page, per_page=msg_per_page.msg_per_page)

    next_page_button = url_for("msgs.msg_inbox", page=msgs_received.next_num) if msgs_received.next_num else None
    previous_page_button = url_for("msgs.msg_inbox", page=msgs_received.prev_num) if msgs_received.prev_num else None

    # Multiple delete form
    form = MessageMultipleDelete()

    if form.validate_on_submit():
        del_lst = request.form.getlist("multi_del")

        if len(del_lst) == 0:
            flash("No messages selected", "warning")
            return redirect(url_for("msgs.msg_inbox"))

        for i in del_lst:
            msg_id = Messages.query.get_or_404(i)
            msg_id.del_in = 1
            db.session.add(msg_id)

        db.session.commit()

        flash("All selected messages were deleted.", "success")

        return redirect(url_for("msgs.msg_inbox"))

    return render_template("msg_inbox.html",
                           msgs_received=msgs_received,
                           next_page_button=next_page_button,
                           previous_page_button=previous_page_button,
                           form=form,
                           get_unread_msgs=get_unread_msgs)


@msgs.route("/msg_outbox", methods=["POST", "GET"])
@login_required
def msg_outbox():
    """
    Get messages for OUTBOX page. Show only messages where the sender username is the current logged in user
    """

    page = request.args.get("page", 1, type=int)
    msg_per_page = User.query.get_or_404(current_user.id)

    # Get the number of unread messages
    get_unread_msgs = unread_msgs(current_user.username)

    msgs_sent = Messages.query. \
        order_by(Messages.date.desc()). \
        filter_by(sender=current_user.username, del_out=False). \
        paginate(page=page, per_page=msg_per_page.msg_per_page)

    next_page_button = url_for("msgs.msg_outbox", page=msgs_sent.next_num) if msgs_sent.next_num else None
    previous_page_button = url_for("msgs.msg_outbox", page=msgs_sent.prev_num) if msgs_sent.prev_num else None

    # Multiple delete form
    form = MessageMultipleDelete()

    if form.validate_on_submit():
        del_lst = request.form.getlist("multi_del")

        if len(del_lst) == 0:
            flash("No messages selected", "warning")
            return redirect(url_for("msgs.msg_outbox"))

        for i in del_lst:
            msg_id = Messages.query.get_or_404(i)
            msg_id.del_out = 1
            db.session.add(msg_id)

        db.session.commit()

        flash("All selected messages were deleted.", "success")

        return redirect(url_for("msgs.msg_outbox"))

    return render_template("msg_outbox.html", msgs_sent=msgs_sent, next_page_button=next_page_button,
                           previous_page_button=previous_page_button, form=form, get_unread_msgs=get_unread_msgs)


@msgs.route("/msg_read/<int:mid>", methods=["POST", "GET"])
@login_required
def msg_read(mid):
    """
    This is the message page. The only available messages are the ones where sender or recipient is the current
    username logged in. Other MIDs (Message IDs) give 404 error (if the user forces another mid)

    If the current logged in users reads a message from the inbox, it automatically marks it as MSG READ.

    :param mid: current message ID
    :return:
    """

    # Get the number of unread messages
    get_unread_msgs = unread_msgs(current_user.username)

    try:
        # get the current message from inbox or outbox and if not deleted
        m_read = Messages.query. \
            filter(Messages.mid == mid). \
            filter((Messages.recipient == current_user.username) & (Messages.del_in == 0) | (
                    Messages.sender == current_user.username) & (Messages.del_out == 0)). \
            first()

        # mark the inbox message as read when the message is opened
        if m_read.recipient == current_user.username:
            m_read.seen = True
            db.session.add(m_read)
            db.session.commit()

        # delete the specific message and return to inbox or outbox
        form = DeleteSingleMessageButton()

        if form.validate_on_submit():
            msg_del = Messages.query.get_or_404(mid)

            if msg_del.recipient == current_user.username:
                msg_del.del_in = True

                db.session.add(msg_del)
                db.session.commit()

                return redirect(url_for("msgs.msg_inbox"))
            else:
                msg_del.del_out = True

                db.session.add(msg_del)
                db.session.commit()

                return redirect(url_for("msgs.msg_outbox"))

        return render_template("msg_read.html", msg_read=m_read, form=form, get_unread_msgs=get_unread_msgs)
    except AttributeError:
        # Get the number of unread messages
        get_unread_msgs = unread_msgs(current_user.username)
        return render_template("errors/404.html", get_unread_msgs=get_unread_msgs)


@msgs.route("/msg_send", methods=["POST", "GET"])
@login_required
def msg_send():
    """
    Send message based on the Username entered. Checks if the introduced username exists in the database. IF the
    user does not exist, it gives a warning and the message is kept in the current form for more editing.
    IF the message was successfully sent then the form is reset.
    """

    form = SendMessageForm()  # Get the current Send Message Form

    # Get the number of unread messages
    get_unread_msgs = unread_msgs(current_user.username)

    if form.validate_on_submit():
        try:
            # Check if username exists
            get_username_record = User.query.filter_by(username=form.send_to.data).first()

            # If everything is OK, add message to DB
            message = Messages(recipient=get_username_record.username,
                               sender=current_user.username,
                               subject_msg=form.subject.data,
                               body_msg=form.msg_body.data,
                               date=datetime.now(),
                               seen=False,
                               del_in=False,
                               del_out=False)

            db.session.add(message)
            db.session.commit()

            flash("Message sent.", "success")
            return redirect(url_for('msgs.msg_send'))
        except AttributeError:
            # Get error if username is invalid or does not exist
            flash("Username " + form.send_to.data + " not found.", "danger")

    return render_template("msg_send.html", form=form, get_unread_msgs=get_unread_msgs)


@msgs.route("/msg_<int:mid>/update", methods=["POST", "GET"])
@login_required
def msg_update(mid):
    """
    Marks the current message as unread. Updates the `seen` column from database from False to True.

    :param mid: current message ID
    :return:
    """

    msg_upd = Messages.query.get_or_404(mid)

    msg_upd.seen = False

    db.session.add(msg_upd)
    db.session.commit()

    return redirect(url_for("msgs.msg_inbox"))
