from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
from flask import request, render_template, current_app, redirect, url_for
from contester.auth.models import ModelEncoder
from email.message import EmailMessage
from passlib.hash import sha256_crypt
from flask import Blueprint
from os import environ
import smtplib

app = Blueprint('auth_bp', __name__, template_folder='templates', static_folder='static')

url_serializer = URLSafeTimedSerializer(environ.get('SECRET_KEY'))
EMAIL_ADDRESS = environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = environ.get('EMAIL_PASSWORD')


@app.record
def record(state):
    db = state.app.config.get('users.db')

    if db is None:
        raise Exception("This blueprint expects you to provide database access through users.db")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session = current_app.config['session']
        users_db = current_app.config['users.db']

        username = request.form.get('username')
        password = request.form.get('password')

        user = users_db.find_user_by_username(username)

        if user is None:
            return render_template('auth/login.html')

        is_password_correct = sha256_crypt.verify(password, user.password)
        if not is_password_correct:
            return render_template('auth/login.html')

        session['user'] = ModelEncoder().encode(user)
        return redirect(url_for('problems_bp.archive'))

    return render_template('auth/login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        unverified_users_db = current_app.config['unverified_users.db']
        users_db = current_app.config['users.db']

        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        is_username_exist = users_db.find_user_by_username(username)
        is_email_exist = users_db.find_user_by_email(email)

        if is_username_exist or is_email_exist:
            return render_template('auth/register.html')

        token = url_serializer.dumps(email, salt='email-confirm')
        token_link = url_for('auth_bp.confirm_email', token=token, _external=True)
        msg = EmailMessage()
        msg['Subject'] = 'Email verification'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = email
        msg.set_content('Your verification link is %s' % token_link)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

        hashed_password = sha256_crypt.hash(password)
        unverified_users_db.create_unverified_user(username, hashed_password, email)

        return '<h1>Verification link was sent to your email</h1>'

    else:
        return render_template('auth/register.html')


@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = url_serializer.loads(token, salt='email-confirm', max_age=3600)
    except SignatureExpired:
        return '<h1>The token is expired!</h1>'
    except BadTimeSignature:
        return '<h1>This isn\'t the right token</h1>'

    unverified_users_db = current_app.config['unverified_users.db']
    unverified_user = unverified_users_db.find_user_by_email(email)
    if unverified_user is None:
        return '<h1>Email not found</h1>'

    users_db = current_app.config['users.db']
    users_db.create_user(unverified_user.username, unverified_user.password, unverified_user.email)

    unverified_users_db.delete_unverified_user_by_email(email)

    return redirect(url_for('auth_bp.login'))


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session = current_app.config['session']

    if 'user' in session:
        session.pop('user')

    return redirect(url_for('auth_bp.login'))