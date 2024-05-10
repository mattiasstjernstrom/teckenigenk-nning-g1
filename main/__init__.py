from flask import Blueprint, render_template

# Blueprint for main routes:
main = Blueprint("main", __name__)


# Main site route:
@main.route("/")
def home():
    return render_template("main/index.html")


"""Api route, to check the drawing area, this might be an blueprint but for now it's just a route."""


@main.route("/api")
def api():
    return "API is working!"
