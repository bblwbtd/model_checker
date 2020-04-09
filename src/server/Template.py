import json

from flask import Blueprint, request, render_template, jsonify

from src.database import Template

template = Blueprint('template', __name__, url_prefix='/template')


@template.route('/add', methods=['GET'])
def get_page():
    return render_template('CreateTemplate.html', title="New Template")


@template.route('/update', methods=['POST'])
def update_template():
    t = Template(id=request.json.get('id', -1))
    t.content = json.dumps(request.json)
    t.save()
    return 'success'


@template.route('/edit', methods=['GET'])
def edit_template():
    templates = [
        {
            'id': t.id,
            'name': t.name
        }
        for t in Template.select()
    ]
    return render_template('EditTemplate.html', templates=templates, title='Edit Template')


@template.route("/add", methods=['POST'])
def add_template():
    body = request.json

    states = body.get('states', None)
    events = body.get('events', None)
    name = body.get('name', '')

    if name == "" or states is None or events is None:
        return "Missing parameters can not be empty", 400

    t = Template(name=name, content=json.dumps(body))
    t.save()
    return "success", 200


@template.route("/remove", methods=['POST'])
def remove_template():
    pass


@template.route("/get", methods=['GET'])
def get_template():
    id = request.args.get("id", None)
    if not id:
        return "unknown id", 400

    template = Template.get(id=id)
    return jsonify(template.content)
