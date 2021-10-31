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

    class AttemptsDBO(object):
        pass

    return AttemptsDBO()
