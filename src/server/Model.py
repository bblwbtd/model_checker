from flask import Blueprint, render_template

model = Blueprint('model', __name__, url_prefix="/model")


@model.route("/check")
def check():
    pass


@model.route("/", methods=['GET'])
def get_model_page():
    return render_template('ModelVerification.html')
