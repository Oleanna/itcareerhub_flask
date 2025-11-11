from flask import Flask

from src.core.app_runner import create_app


app = Flask(__name__)
create_app(app)


if __name__ == "__main__":
    app.run(debug=True)

