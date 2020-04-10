from flask import Flask, render_template

from src.server.Model import model
from src.server.Template import template

app = Flask(__name__)
app.register_blueprint(template)
app.register_blueprint(model)


@app.route('/', methods=['GET'])
def get_index():
    return render_template('Index.html')


@app.route('/introduction', methods=['GET'])
def get_introduction():
    return render_template('Introduction.html')
