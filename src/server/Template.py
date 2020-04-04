import json

from flask import Blueprint, request, render_template

from src.database import Template, MagicTemplate
from src.server.Parser import parse_validator, parse_state, parse_event

template = Blueprint('template', __name__, url_prefix='/template')


@template.route('/add', methods=['GET'])
def get_page():
    return render_template('CreateTemplate.html')


@template.route("/all", methods=['GET'])
def get_all_template():
    pass


@template.route("/add", methods=['POST'])
def add_template():
    body = json.load(request.data)
    variable = body.get('variable', {})

    states = body.get('states', None)
    events = body.get('events', None)

    state_instances = [parse_state(i, variable) for i in events]
    event_instances = [parse_event(i, variable) for i in states]

    validator = parse_validator(body.get('validator', ''), variable)

    magic_template = MagicTemplate(validator, variable, state_instances, event_instances)
    Template(content=magic_template.serialize()).save()


@template.route("/remove", methods=['POST'])
def remove_template():
    pass
