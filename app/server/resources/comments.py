from flask import Blueprint, request, Response
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow.exceptions import ValidationError
from mongoengine.errors import OperationError

from server import db, ma
from server.database.models import User, Card, Comment
from server.database.schemas import CommentSchema


class CommentsAPI(MethodView):
    def get(self, card_id, comment_id):
        card = Card.objects.get_or_404(id=card_id)

        if comment_id is None:
            resp = CommentSchema(many=True).dumps(card.content)
            return Response(resp, mimetype="application/json", status=200)

        for comment in card.content:
            if str(comment.id) == comment_id:
                break
        else:  # no-break
            return '', 404

        resp = CommentSchema().dumps(comment)
        return Response(resp, mimetype="application/json", status=200)

    @jwt_required()
    def post(self, card_id):
        try:
            user_id = get_jwt_identity()
            user = User.objects.get(id=user_id)
            card = Card.objects.get_or_404(id=card_id, owner=user)

            data = request.get_json(force=True)
            data = CommentSchema().load(data)
            comment = Comment(**data, sender=user)
            card.update(push__content=comment)
            card.save()
            return CommentSchema().dump(data), 200
        except ValidationError as e:
            return {'errors': e.messages}, 400

    @jwt_required()
    def put(self, card_id, comment_id):
        try:
            user_id = get_jwt_identity()
            user = User.objects.get(id=user_id)
            card = Card.objects.get_or_404(id=card_id, owner=user)

            for comment in card.content:
                if str(comment.id) == comment_id:
                    break
            else:  # no-break
                return '', 404

            data = request.get_json(force=True)
            data = CommentSchema().load(data, partial=True)
            comment.text = data['text']
            card.save()
            return data, 200
        except ValidationError as e:
            return {'errors': e.messages}, 400

    @jwt_required()
    def delete(self, card_id, comment_id):
        try:
            user_id = get_jwt_identity()
            user = User.objects.get(id=user_id)
            card = Card.objects.get_or_404(id=card_id, owner=user)

            for comment in card.content:
                if str(comment.id) == comment_id:
                    break
            else:  # no-break
                return '', 404

            card.content.remove(comment)
            card.save()
            return {'status': 'success'}, 200
        except OperationError as e:
            return {'errors': 'Operational error'}, 400

comments_view = CommentsAPI.as_view('comments')

blueprint = Blueprint("comments", __name__, url_prefix="/cards")
blueprint.add_url_rule('/<string:card_id>/comments/', view_func=comments_view, defaults={'comment_id': None}, methods=['GET'])
blueprint.add_url_rule('/<string:card_id>/comments/', view_func=comments_view, methods=['POST'])
blueprint.add_url_rule('/<string:card_id>/comments/<string:comment_id>', view_func=comments_view, methods=['GET', 'PUT', 'DELETE'])
