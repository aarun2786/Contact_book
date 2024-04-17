from main import main as mian_blueprint
from flask import Flask
from file_manager import paths


def create_app():
    app = Flask(__name__)
    app.secret_key = 'akr'
    app.config['UPLOAD_FOLDER'] = paths
    app.register_blueprint(mian_blueprint)
    return app

if __name__ == "__main__":
    create_app().run(debug=True)
