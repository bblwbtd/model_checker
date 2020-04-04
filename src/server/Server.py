from flask import Flask, render_template

from src.server.Template import template

app = Flask(__name__)
app.register_blueprint(template)


@app.route('/', methods=['GET'])
def get_index():
    return render_template('Index.html')
