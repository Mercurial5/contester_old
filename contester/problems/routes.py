from flask import Blueprint, render_template, current_app, redirect, url_for
import json


app = Blueprint('problems_bp', __name__, template_folder='templates', static_folder='static')


@app.route('/archive')
def archive():
    session = current_app.config['session']

    if 'user' in session:
        user = session['user']
        return render_template('problems/archive.html', user=user)
    else:
        return redirect(url_for('auth_bp.login'))
