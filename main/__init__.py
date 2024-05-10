from flask import Blueprint

# Blueprint for main routes:
main = Blueprint("main", __name__)


@main.route("/")
def home():
    return "Drawing area"
