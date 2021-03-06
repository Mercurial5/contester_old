from flask import Blueprint, render_template, current_app, redirect, url_for, request
from datetime import datetime
import json

app = Blueprint('problems_bp', __name__, template_folder='templates', static_folder='static')


@app.route('/archive')
def archive():
    session = current_app.config['session']

    if 'user' in session:
        user = session['user']

        problems_db = current_app.config['problems.db']
        problems = problems_db.get_first_n_problems(10)

        return render_template('problems/archive.html', user=user, problems=problems)
    else:
        return redirect(url_for('auth_bp.login'))


@app.route('/problem_page/<problem_id>')
def problem_page(problem_id):
    session = current_app.config['session']

    if 'user' not in session:
        return redirect(url_for('auth_bp.login'))

    problems_db = current_app.config['problems.db']
    samples_db = current_app.config['samples.db']
    attempts_db = current_app.config['attempts.db']

    user = session['user']
    problem = problems_db.get_problem_by_id(problem_id)

    samples = samples_db.get_first_n_samples(problem_id, problem.samples_count)
    attempts = attempts_db.get_attempts(user['id'], problem_id)
    attempts = [give_color_to_attempt(attempt) for attempt in attempts]

    attempt_counts = attempts_db.get_attempts_count(user['id'], problem_id)

    payload = json.dumps({'problem_id': problem.id, 'host': request.host})

    return render_template('problems/problem_page.html', problem=problem, user=user, samples=samples, payload=payload,
                           attempts=attempts, attempt_counts=attempt_counts)


@app.route('/save_attempt', methods=['POST'])
def save_attempt():
    session = current_app.config['session']
    attempts_db = current_app.config['attempts.db']
    post_data = json.loads(request.data.decode('utf-8'))

    user_id = session['user']['id']
    post_data['accepted'] = False if post_data['status'] is False else post_data.get('accepted')
    post_data['submitted_time'] = datetime.fromtimestamp(post_data['submitted_time'])

    attempt_id = attempts_db.save_new_attempt(user_id, post_data)
    return {'attempt_id': attempt_id}


@app.route('/show_attempt/<attempt_id>', methods=['GET'])
def show_attempt(attempt_id):
    attempts_db = current_app.config['attempts.db']

    attempt = attempts_db.get_attempt(attempt_id)

    print(attempt.code)
    return render_template('problems/show_attempt.html', code=attempt.code, log=attempt.log)


def give_color_to_attempt(attempt):
    if attempt.status is False:
        color_name = 'error-attempt'
    elif attempt.accepted is True:
        color_name = 'accepted-attempt'
    else:
        color_name = 'wrong-attempt'

    attempt.color_name = color_name

    return attempt
