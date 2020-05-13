from core.models import Messages


def unread_msgs(current_acc_uname):
    gum = Messages.query.filter_by(recipient=current_acc_uname, del_in=False, seen=False).count()

    return gum