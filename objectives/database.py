import os
import requests
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


DATASERVICE=os.environ['DATA_SERVICE']
db = SQLAlchemy()


class Objective(db.Model):
    __tablename__ = 'objective'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode(128))
    target_distance = db.Column(db.Float)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer)

    @staticmethod
    def to_datetime(date_str):
        return datetime.fromtimestamp(float(date_str))

    @property
    def completion(self):
        runs = requests.get(DATASERVICE + '/runs?user_id='+str(self.user_id) +
                            '&from_date='+self.start_date.timestamp() +
                            '&to_date='+self.start_date.timestamp()).json()
        return min(round(100 * (sum([run.distance for run in runs]) / self.target_distance), 2), 100)

    def to_json(self):
        res = {}
        for attr in ('id', 'name', 'target_distance', 'start_date',
                     'end_date', 'user_id'):
            value = getattr(self, attr)
            if isinstance(value, datetime):
                value = value.timestamp()
            res[attr] = value
            #res['completion'] = self.completion()
        return res
