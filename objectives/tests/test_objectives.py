from objectives.tests.utility import client, new_objective
from objectives.database import db, Objective


def test_add_user(client):
    tested_app, app = client

    objective = new_objective()
    json = objective.to_json()

    # Add a new objective
    assert tested_app.post('/objectives', json=json).status_code == 200
    #with app.app_context():
    #    db_objective = db.session.query(Objective).filter(Objective.id == objective.id).first()
    #    assert db_objective == objective
