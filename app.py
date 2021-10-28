from contester.auth import setup_default_user_db
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask import Flask
from os import environ


def create_app() -> Flask:
    load_dotenv()

    app = Flask(__name__)

    with app.app_context():
        app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLALCHEMY_DATABASE_URI')
        db = SQLAlchemy(app)

        app.config['users.db'] = setup_default_user_db(db)

        db.create_all()

        from contester.auth import auth_app
        app.register_blueprint(auth_app, url_prefix='/auth')

        return app
