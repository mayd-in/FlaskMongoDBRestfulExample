from flask import Blueprint, request, Response
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow.exceptions import ValidationError
from mongoengine.errors import OperationError

from server import db, ma
from server.database.models import User, Card, Comment
from server.database.schemas import CardSchema, CommentSchema


class CardsAPI(MethodView):
    def get(self, card_id):
        card = Card.objects.get_or_404(id=card_id)
        resp = CardSchema().dumps(card)
        return Response(resp, mimetype="application/json", status=200)

    @jwt_required()
    def put(self, card_id):
        try:
            user_id = get_jwt_identity()
            user = User.objects.get(id=user_id)
            card = Card.objects.get_or_404(id=card_id, owner=user)

            data = request.get_json(force=True)
            data = CardSchema().load(data, partial=True)
            card.update(**data)
            card.save()
            return data, 200
        except ValidationError as e:
            return {'errors': e.messages}, 400

    @jwt_required()
    def delete(self, card_id):
        try:
            user_id = get_jwt_identity()
            user = User.objects.get(id=user_id)
            card = Card.objects.get_or_404(id=card_id, owner=user)
            card.delete()
            return {'status': 'success'}, 200
        except OperationError as e:
            return {'errors': 'Operational error'}, 400

cards_view = CardsAPI.as_view('cards')

blueprint = Blueprint("cards", __name__, url_prefix="/cards")
blueprint.add_url_rule('/<string:card_id>', view_func=cards_view, methods=['GET', 'PUT', 'DELETE'])
