import os
import requests_mock
from datetime import datetime, timedelta
from objectives.tests.utility import client, new_objective, new_run_json
from objectives.database import db, Objective


DATASERVICE=os.environ['DATA_SERVICE']


def test_objective(client):
    tested_app, app = client

    with requests_mock.mock() as m:
        m.get(DATASERVICE + '/runs?user_id=1', json=[])

        # Add a new objective in database
        objective = new_objective()
        json = objective.to_json()
        objective.id = 1  # it will have id 1

        import requests
        runs = requests.get(DATASERVICE + '/runs?user_id='+str(objective.id)).json()
        print(runs)

        # Add a new objective
        assert tested_app.post('/objectives', json=json).status_code == 200

        # Check that it exists in the database
        with app.app_context():
            db_objective = db.session.query(Objective).filter(Objective.id == objective.id).first()
            assert db_objective.to_json() == objective.to_json()


def test_get_objective(client):
    tested_app, app = client

    # Add a new objective in database
    objective = new_objective()
    with app.app_context():
        db.session.add(objective)
        db.session.commit()
        objective = db.session.query(Objective).first()

    with requests_mock.mock() as m:
        m.get(DATASERVICE + '/runs?user_id=1', json=[])

        # Check that exists an objective with id 1
        first_objective = tested_app.get('/objectives/'+str(objective.id)).json
        assert first_objective == objective.to_json()

        # Try to retrieve a non existing objective
        assert tested_app.get('/objectives/-1').status_code == 404


def test_get_user_objectives(client):
    tested_app, app = client

    # Add a new objective in database
    objective = new_objective()
    with app.app_context():
        db.session.add(objective)
        db.session.commit()
        objective = db.session.query(Objective).first()

    with requests_mock.mock() as m:
        m.get(DATASERVICE + '/runs?user_id=1', json=[])

        # Check that the objective exists for the user
        user_objectives = tested_app.get('/objectives?user_id='+str(objective.user_id)).json
        assert user_objectives[0] == objective.to_json()

        # Try to retrieve the objective list without passing the user
        assert tested_app.get('/objectives').status_code == 400

        # Try to retrieve the objective list of a non existing user
        user_objectives = tested_app.get('/objectives?user_id=-1').json
        assert len(user_objectives) == 0


def test_completion(client):
    tested_app, app = client

    # Add a new objective in database
    objective = new_objective()
    with app.app_context():
        db.session.add(objective)
        db.session.commit()
        objective = db.session.query(Objective).first()

    # Prepare some runs
    run_before = new_run_json(run_id=1, date=(datetime.now() - timedelta(days=5)).timestamp())
    run_ok = new_run_json(run_id=2, date=(datetime.now() + timedelta(days=1)).timestamp())
    run_after = new_run_json(run_id=3, date=(datetime.now() + timedelta(days=10)).timestamp())

    with requests_mock.mock() as m:
        m.get(DATASERVICE + '/runs?user_id=1', json=[run_before, run_ok, run_after])

        # Check that exists an objective with id 1
        first_objective = tested_app.get('/objectives/'+str(objective.id)).json
        assert first_objective['completion'] == objective.completion
        expected_completion = min(round(100 * run_ok['distance'] / objective.target_distance, 2), 100)
        assert first_objective['completion'] == expected_completion


def test_delete(client):
    tested_app, app = client

    # Add a new objective in database
    objective = new_objective()
    with app.app_context():
        db.session.add(objective)
        db.session.add(objective)
        db.session.commit()
        objective = db.session.query(Objective).first()

    # Delete it
    assert tested_app.delete('/objectives?user_id=1').status_code == 200

    # Check that it doesn't exist in the database
    with app.app_context():
        assert not db.session.query(Objective).filter(Objective.id == objective.id).first()

    # Check that the objective doesn't exist for the user
    user_objectives = tested_app.get('/objectives?user_id='+str(objective.user_id)).json
    assert len(user_objectives) == 0
