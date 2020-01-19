from hero import db

class Subscription(db.Model):
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return "Subscribers: {}".format(self.email)
