import os
from flakon import SwaggerBlueprint
from flask import request, jsonify, make_response
from objectives.database import db, Objective

HERE = os.path.dirname(__file__)
YML = os.path.join(HERE, '..', 'static', 'api.yaml')
api = SwaggerBlueprint('API', __name__, swagger_spec=YML)


@api.operation('getObjectives')
def get_objectives(user_id):
    objectives = db.session.query(Objective).filter(Objective.runner_id == user_id)
    return jsonify([objective.to_json() for objective in objectives])


@api.operation('createObjective')
def create_objective():
    req = request.json
    objective = Objective()
    objective.user_id = req['user_id']
    objective.name = req['name']
    objective.target_distance = req['target_distance']
    objective.start_date = objective.to_datetime(req['start_date'])
    objective.end_date = objective.to_datetime(req['end_date'])
    db.session.add(objective)
    db.session.commit()
    return make_response("ok")


@api.operation('getObjective')
def get_objective(objective_id):
    objective = db.session.query(Objective).filter(Objective.id == objective_id)
    return objective.to_json()
