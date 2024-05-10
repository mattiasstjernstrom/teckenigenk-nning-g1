from flask import Blueprint

# Blueprint for main routes:
main = Blueprint("main", __name__)


# Main site route:
@main.route("/")
def home():
    return "Drawing area"


# Api route, to check the drawing area:
@main.route("/api")
def api():
    return "Api route"
