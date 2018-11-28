from datetime import datetime
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Objective(db.Model):
    __tablename__ = 'objective'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode(128))
    target_distance = db.Column(db.Float)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    runner_id = db.Column(db.Integer)

    ''''
    @property
    def completion(self):
        runs = db.session.query(Run) \
            .filter(Run.start_date > self.start_date) \
            .filter(Run.start_date <= self.end_date) \
            .filter(Run.runner_id == self.runner_id)

        return min(round(100 * (sum([run.distance for run in runs]) / self.target_distance), 2), 100)
    '''

    def to_json(self):
        res = {}
        for attr in ('id', 'name', 'target_distance', 'start_date',
                     'end_date', 'runner_id'):
            value = getattr(self, attr)
            if isinstance(value, datetime):
                value = value.timestamp()
            res[attr] = value
        return res
