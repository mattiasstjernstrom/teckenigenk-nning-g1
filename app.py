from flask import Flask

app = Flask(__name__)

# Blueprint for main routes:
from main import main as main_routes

app.register_blueprint(main_routes)


if __name__ == "__main__":
    app.run(debug=True, port="5000")
