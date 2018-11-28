import pytest
import os
import tempfile
from datetime import datetime, timedelta
from objectives.app import create_app
from objectives.database import db, Objective


@pytest.fixture
def client():
    """ This function initialize a new DB for every test and creates the app. This function returns a tuple,
    the first element is a test client and the second is the app itself. Test client must be used for sending
    request and the app should be used for getting a context when, for example, we need to query the DB.
    I haven't found a more elegant way to do this."""
    app = create_app()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+app.config['DATABASE']
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # disable CSRF validation -> DO THIS ONLY DURING TESTS!

    client = app.test_client()

    db.create_all(app=app)
    db.init_app(app=app)

    yield client, app

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


def new_objective(user_id=1):
    objective = Objective()
    objective.name = "Test"
    objective.target_distance = 100000.0
    objective.start_date = datetime.now()
    objective.end_date = datetime.now() + timedelta(days=7)
    objective.user_id = user_id
    return objective


def new_run_json(run_id=1, date=datetime.now()):
    return {
        "id": run_id,
        "user_id": 1,
        "strava_id": 1956250882+run_id,
        "title": "Test Run",
        "distance": 50000.0,
        "description": None,
        "average_speed": 10.0,
        "elapsed_time": 5000.0,
        "total_elevation_gain": 3.0,
        "average_heartrate": None,
        "start_date": date,
    }
