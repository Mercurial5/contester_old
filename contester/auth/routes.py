from flask import request, render_template, current_app, redirect, url_for
from passlib.hash import sha256_crypt
from flask import Blueprint

app = Blueprint('auth_bp', __name__, template_folder='templates', static_folder='static')


@app.record
def record(state):
    db = state.app.config.get('users.db')

    if db is None:
        raise Exception("This blueprint expects you to provide database access through users.db")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        db = current_app.config['users.db']

        username = request.form.get('username')
        password = request.form.get('password')

        user = db.find_user_by_username(username)

        if user is None:
            return render_template('auth/login.html')

        is_password_correct = sha256_crypt.verify(password, user.password)
        if not is_password_correct:
            return render_template('auth/login.html')

        return 'You have passed.'

    return render_template('auth/login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        db = current_app.config['users.db']

        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        is_username_exist = db.find_user_by_username(username)
        is_email_exist = db.find_user_by_email(email)

        if is_username_exist or is_email_exist:
            return render_template('auth/register.html')

        hashed_password = sha256_crypt.hash(password)
        print(hashed_password)
        db.create_user(username, hashed_password, email)

        return redirect(url_for('auth_bp.login'))

    else:
        return render_template('auth/register.html')
