from flask_sqlalchemy import SQLAlchemy
from typing import List


def setup_problems_db(db: SQLAlchemy):
    class Problems(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(60), nullable=False)
        description = db.Column(db.Text, nullable=False)
        samples_count = db.Column(db.Integer, nullable=False)

        def __repr__(self):
            return '<Problems %r>' % self.name

    class ProblemsDBO(object):
        def get_problem_by_id(self, id: int) -> Problems:
            return Problems.query.filter(Problems.id == id).first()

        def get_first_n_problems(self, n: int) -> List[Problems]:
            return Problems.query.limit(n).all()

    return ProblemsDBO()


def setup_samples_db(db: SQLAlchemy):
    class Samples(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        problem_id = db.Column(db.Integer, nullable=False, index=True)
        input = db.Column(db.Text)
        output = db.Column(db.Text, nullable=False)

        def __repr__(self):
            return '<Samples %d>' % self.id

    class SamplesDBO(object):
        def get_samples(self, problem_id: int) -> List[Samples]:
            return Samples.query.filter(Samples.problem_id == problem_id).all()

        def get_first_n_samples(self, problem_id: int, count: int) -> List[Samples]:
            return Samples.query.filter(Samples.problem_id == problem_id).limit(count).all()

    return SamplesDBO()


def setup_attempts_db(db: SQLAlchemy):
    class Attempts(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, nullable=False, index=True)
        problem_id = db.Column(db.Integer, nullable=False, index=True)
        status = db.Column(db.Boolean, nullable=False)
        error = db.Column(db.String(255), nullable=True)
        log = db.Column(db.Text, nullable=True)
        accepted = db.Column(db.Boolean, nullable=False)
        failed_case = db.Column(db.Integer, nullable=True)
        code = db.Column(db.Text, nullable=False)

        def __init__(self, user_id: int, problem_id: int, status: bool, error: str, log: str, accepted: bool,
                     failed_case: int, code: str):
            self.user_id = user_id
            self.problem_id = problem_id
            self.status = status
            self.error = error
            self.log = log
            self.accepted = accepted
            self.failed_case = failed_case
            self.code = code

    class AttemptsDBO(object):
        def save_new_attempt(self, user_id: int, data: dict):
            new_attempt = Attempts(user_id, data['problem_id'], data['status'], data.get('error'),
                                   data.get('log'), data['accepted'], data.get('failed_case', 0), data['code'])

            db.session.add(new_attempt)
            db.session.commit()

        def get_attempts(self, user_id: int, problem_id: int):
            return Attempts.query.filter(Attempts.user_id == user_id, Attempts.problem_id == problem_id).limit(10).all()

        def get_attempts_count(self, user_id: int, problem_id: int):
            return Attempts.query.filter(Attempts.user_id == user_id, Attempts.problem_id == problem_id).count()

    return AttemptsDBO()
