from flask import Flask, request, render_template, current_app
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
        if user is None or user.password != password:
            return render_template('auth/login.html')

        return 'You have passed.'

    return render_template('auth/login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return 'so?'
    else:
        return render_template('auth/register.html')