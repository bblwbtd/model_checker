from flask import Blueprint, request, render_template

from src.database import Template

template = Blueprint('template', __name__, url_prefix='/template')


@template.route('/add', methods=['GET'])
def get_page():
    return render_template('CreateTemplate.html', title="New Template")


@template.route("/all", methods=['GET'])
def get_all_template():
    pass


@template.route("/add", methods=['POST'])
def add_template():
    body = request.json

    states = body.get('states', None)
    events = body.get('events', None)
    name = body.get('name', '')

    if name == "" or states is None or events is None:
        return "Missing parameters can not be empty", 400

    t = Template(name=name, content=body)
    t.save()
    return "success", 200


@template.route("/remove", methods=['POST'])
def remove_template():
    pass
