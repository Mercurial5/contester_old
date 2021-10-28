from flask_sqlalchemy import SQLAlchemy


def setup_unverified_users_db(db: SQLAlchemy):
    class UnverifiedUsers(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True, nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)
        password = db.Column(db.String(255), unique=True, nullable=False)

        def __init__(self, username: str, password: str, email: str):
            self.username = username
            self.password = password
            self.email = email

        def __repr__(self):
            return '<UnverifiedUsers %r>' % self.username

    class UnverifiedUsersDBO(object):
        def create_unverified_user(self, username: str, password: str, email: str):
            unverified_user = UnverifiedUsers(username, password, email)
            db.session.add(unverified_user)
            db.session.commit()

        def find_user_by_email(self, email: str) -> UnverifiedUsers:
            return UnverifiedUsers.query.filter(UnverifiedUsers.email == email).first()

    return UnverifiedUsersDBO()


def setup_users_db(db: SQLAlchemy):
    class Users(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True, nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)
        password = db.Column(db.String(255), unique=True, nullable=False)

        def __init__(self, username: str, password: str, email: str):
            self.username = username
            self.password = password
            self.email = email

        def __repr__(self):
            return '<User %r>' % self.username

    class UsersDBO(object):
        def find_user_by_id(self, user_id: int) -> Users:
            return Users.query.filter(Users.id == user_id).first()

        def find_user_by_username(self, username: str) -> Users:
            return Users.query.filter(Users.username == username).first()

        def find_user_by_email(self, email: str) -> Users:
            return Users.query.filter(Users.email == email).first()

        def create_user(self, username: str, password: str, email: str):
            user = Users(username, password, email)
            db.session.add(user)
            db.session.commit()

    return UsersDBO()
