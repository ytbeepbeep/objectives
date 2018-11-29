import os
from flakon import SwaggerBlueprint
from flask import request, jsonify, make_response, abort
from objectives.database import db, Objective

HERE = os.path.dirname(__file__)
YML = os.path.join(HERE, '..', 'static', 'api.yaml')
api = SwaggerBlueprint('API', __name__, swagger_spec=YML)


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
    objective = db.session.query(Objective).filter(Objective.id == objective_id).first()
    if not objective:
        abort(404)
    return objective.to_json()


@api.operation('getObjectives')
def get_objectives():
    user_id = request.args.get("user_id")
    if not user_id:
        abort(400)

    objectives = db.session.query(Objective).filter(Objective.user_id == user_id)
    return jsonify([objective.to_json() for objective in objectives])

@api.operation('deleteObjectives')
def delete_objectives():
    user_id = request.args.get('user_id')
    if not user_id:
        abort(400)
    objectives = db.session.query(Objective).filter(Objective.user_id == user_id).all()
    if not objectives:
        return abort(404)

    for obj in objectives:
        db.session.delete(obj)
    db.session.commit()
    return make_response('OK')