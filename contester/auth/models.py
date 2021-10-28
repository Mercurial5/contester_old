from flask_sqlalchemy import SQLAlchemy


def setup_default_user_db(db: SQLAlchemy):
    class Users(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True, nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)
        password = db.Column(db.String(255), unique=True, nullable=False)

        def __init__(self, id: int, username: str, email: str):
            self.id = id
            self.username = username
            self.email = email

        def __repr__(self):
            return '<User %r>' % self.username

    class UserDBO(object):
        def find_user_by_id(self, user_id: int) -> Users:
            return Users.query.filter(Users.id == user_id).first()

        def find_user_by_username(self, username: str) -> Users:
            return Users.query.filter(Users.username == username).first()

    return UserDBO()
