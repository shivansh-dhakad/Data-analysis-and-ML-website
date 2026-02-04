from flask import Flask
from controllers.code import code
SECRET_KEY = "a8f9d7s6g5h4j3k2l1q0w9e8r7t6y5u5"

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.secret_key = SECRET_KEY
    app.register_blueprint(code)
    return app

if __name__ == "__main__":
    app = create_app()
    # debug True for development only
    app.run(host="0.0.0.0", port=5000, debug=True)