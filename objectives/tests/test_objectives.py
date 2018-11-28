from objectives.tests.utility import client, new_objective
from objectives.database import db, Objective


def test_objective(client):
    tested_app, app = client

    objective = new_objective()
    json = objective.to_json()
    objective.id = 1  # it will have id 1

    # Add a new objective and check that exists
    assert tested_app.post('/objectives', json=json).status_code == 200
    with app.app_context():
        db_objective = db.session.query(Objective).filter(Objective.id == objective.id).first()
        assert db_objective.to_json() == objective.to_json()


def test_get_objective(client):
    tested_app, app = client

    objective = new_objective()
    with app.app_context():
        db.session.add(objective)
        db.session.commit()
        objective = db.session.query(Objective).first()

    # Check that exists an objective with id 1
    first_objective = tested_app.get('/objectives/'+str(objective.id)).json
    assert first_objective == objective.to_json()

    # Try to retrieve a non existing objective
    assert tested_app.get('/objectives/-1').status_code == 404


def test_get_user_objectives(client):
    tested_app, app = client

    objective = new_objective()
    with app.app_context():
        db.session.add(objective)
        db.session.commit()
        objective = db.session.query(Objective).first()

    # Check that the objective exists for the user
    user_objectives = tested_app.get('/objectives?user_id='+str(objective.user_id)).json
    assert user_objectives[0] == objective.to_json()

    # Try to retrieve the objective list without passing the user
    assert tested_app.get('/objectives').status_code == 400

    # Try to retrieve the objective list of a non existing user
    user_objectives = tested_app.get('/objectives?user_id=-1').json
    assert len(user_objectives) == 0
