from flask import Blueprint, render_template, request, jsonify

from src.database import Template
from src.model_checker import MagicTemplate, State, Event
from src.server.Parser import function_wrapper

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
        State(i['state_name'],
              function_wrapper(i['on_enter_state'], variables),
              function_wrapper(i['on_leave_state'], variables),
              i['is_initial'],
              i['is_final'])
        for i in states.values()
    ]

    event_instances = [
        Event(i['event_name'], i['src'], i['des'], function_wrapper(i['on_event'], variables))
        for i in events.values()
    ]

    t = MagicTemplate(validator, variables, state_instances, event_instances)
    return jsonify(t.dfs_check(max_depth, variables))


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
