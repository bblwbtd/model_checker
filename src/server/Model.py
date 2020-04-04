from flask import Blueprint

model = Blueprint('model', __name__, url_prefix="/api/model")


@model.route("/check")
def check():
    pass
