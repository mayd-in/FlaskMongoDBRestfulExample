from datetime import timedelta

from flask import Blueprint, request
from flask.views import MethodView
from flask_jwt_extended import create_access_token
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist

from server.database.models import User

class RegisterAPI(MethodView):
    def post(self):
        try:
            body = request.get_json()
            user = User(**body)
            user.hash_password()
            user.save()
            return {'id': str(user.id)}, 200
        except FieldDoesNotExist:
            return {'error': 'Request is missing required fields'}, 400
        except NotUniqueError:
            return {'error': 'Email address already exists'}, 400

class LoginAPI(MethodView):
    def post(self):
        try:
            body = request.get_json()
            user = User.objects.get(email=body.get('email'))
            authorized = user.check_password(body.get('password'))
            if not authorized:
                return {'error': 'Email or password invalid'}, 401

            expires = timedelta(days=7)
            access_token = create_access_token(identity=str(user.id), expires_delta=expires)
            return {'token': access_token}, 200
        except DoesNotExist:
            return {'error': 'Email address does not exists'}, 400


registration_view = RegisterAPI.as_view('register_api')
login_view = LoginAPI.as_view('login_api')

blueprint = Blueprint("auth", __name__, url_prefix="/auth")
blueprint.add_url_rule("/register", view_func=registration_view)
blueprint.add_url_rule("/login", view_func=login_view)
