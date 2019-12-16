from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer(), unique=True, nullable=False, primary_key=True)
    uname = db.Column(db.String(64), index=True, unique=True, nullable=False)
    pword_hash = db.Column(db.String(128), unique=False, nullable=False)
    two_fa = db.Column(db.String(11), unique=False, nullable=True)
    admin_role = db.Column(db.Boolean(), unique=False, nullable=False, default=False)

    def __repr__(self):
        return f"User({self.id!r},{self.uname!r},{self.pword_hash!r},{self.two_fa!r},{self.admin_role!r})"

    def set_password(self, pword):
        self.pword_hash = generate_password_hash(pword)

    def check_password(self, pword):
        return check_password_hash(self.pword_hash, pword)

    #def is_admin(self):
    #    return self.admin_role == True

class Spell(UserMixin, db.Model):
    id = db.Column(db.Integer(), unique=True, nullable=False, primary_key=True)
    uname = db.Column(db.String(64), unique=False, nullable=False)
    query_text = db.Column(db.String(100000), unique=False, nullable=False)
    query_results = db.Column(db.String(100000), unique=False, nullable=False)

    def __repr__(self):
        return f"User({self.id!r},{self.uname!r},{self.query_text!r},{self.query_results!r})"

class TimeLog(UserMixin, db.Model):
    id = db.Column(db.Integer(), unique=True, nullable=False, primary_key=True)
    uname = db.Column(db.String(64), unique=False, nullable=False)
    login_time = db.Column(db.DateTime)
    logout_time = db.Column(db.DateTime, default=None)

    def __repr__(self):
        return f"User({self.id!r},{self.uname!r},{self.login_time!r},{self.logout_time!r})"

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
