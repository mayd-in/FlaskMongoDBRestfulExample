import os

from flask import Flask, jsonify
from flask_mongoengine import MongoEngine
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

application = Flask(__name__)

application.config["MONGODB_SETTINGS"] = {
    'db': os.environ['MONGODB_DATABASE'],
    'host': os.environ['MONGODB_HOSTNAME'],
    'port': 27017,
    'username': os.environ['MONGODB_USERNAME'],
    'password': os.environ['MONGODB_PASSWORD'],
}
application.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']

db = MongoEngine(application)
ma = Marshmallow(application)
bcrypt = Bcrypt(application)
jwt = JWTManager(application)

@application.route('/')
def index():
    return jsonify(
        status=True,
        message='Welcome to the Dockerized Flask MongoDB application!'
    )

from .resources import auth, boards, cards, comments
application.register_blueprint(auth.blueprint)
application.register_blueprint(boards.blueprint)
application.register_blueprint(cards.blueprint)
application.register_blueprint(comments.blueprint)

if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    application.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)
