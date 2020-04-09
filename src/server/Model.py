from flask import Blueprint, render_template, request, jsonify

from src.database import Template
from src.model_checker import MagicTemplate
from src.server.Parser import parse_state, parse_event, parse_variable

model = Blueprint('model', __name__, url_prefix="/model")


@model.route("/check", methods=['POST'])
def check():
    body = request.json

    variables = body.get('variables', {})
    events = body.get('events', {})
    states = body.get('states', {})
    validator = body.get('validator', '')
    max_depth = body.get('max_depth', 100)

    state_instances = [
        parse_state(i)
        for i in states.values()
    ]

    event_instances = [
        parse_event(i)
        for i in events.values()
    ]

    variables = parse_variable(variables)

    t = MagicTemplate(validator, variables, state_instances, event_instances)
    return jsonify(t.dfs_check(max_depth))


@model.route("/", methods=['GET'])
def get_model_page():
    templates = [
        {
            'id': template.id,
            'name': template.name
        }
        for template in Template.select()
    ]
    return render_template('ModelVerification.html', templates=templates)
