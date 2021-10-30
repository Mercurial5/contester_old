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
        input = db.Column(db.String)
        output = db.Column(db.String, nullable=False)

        def __repr__(self):
            return '<Samples %d>' % self.id

    class SamplesDBO(object):
        def get_samples(self, problem_id: int) -> List[Samples]:
            return Samples.query.filter(Samples.problem_id == problem_id).all()

    return SamplesDBO()
