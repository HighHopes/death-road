from hero import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.get(int(user_id))


class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return "Email: {}".format(self.email)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return "Username: {}\nEmail: {}".format(self.username, self.email)
