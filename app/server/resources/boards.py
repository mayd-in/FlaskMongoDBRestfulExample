from flask import Blueprint, request, jsonify, Response, make_response
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow.exceptions import ValidationError
from mongoengine.errors import OperationError, NotUniqueError

from server import db, ma
from server.database.models import User, Board, Card
from server.database.schemas import BoardSchema, CardSchema


class BoardsAPI(MethodView):
    def get(self, board_id):
        if board_id is None:
            resp = BoardSchema(many=True).dumps(Board.objects)
            return Response(resp, mimetype="application/json", status=200)

        board = Board.objects.get_or_404(id=board_id)
        resp = BoardSchema().dumps(board)
        return Response(resp, mimetype="application/json", status=200)

    @jwt_required()
    def post(self, board_id):
        try:
            user_id = get_jwt_identity()
            user = User.objects.get(id=user_id)

            data = request.get_json(force=True)

            if board_id is None:  # Add board
                data = BoardSchema().load(data)
                board = Board(**data, owner=user)
                board.save()
                return BoardSchema().dump(board), 200
            else:  # Add card to board
                board = Board.objects.get_or_404(id=board_id)
                data = CardSchema().load(data)
                card = Card(**data, owner=user)
                card.save()
                board.update(push__cards=card)
                board.save()
                return CardSchema().dump(card), 200
        except ValidationError as e:
            return {'errors': e.messages}, 400
        except NotUniqueError:
            return {'error': 'Board name already exists'}, 400

    @jwt_required()
    def put(self, board_id):
        try:
            user_id = get_jwt_identity()
            user = User.objects.get(id=user_id)
            board = Board.objects.get_or_404(id=board_id, owner=user)

            data = request.get_json(force=True)
            data = BoardSchema().load(data, partial=True)
            board.update(**data)
            board.save()
            return data, 200
        except ValidationError as e:
            return {'errors': e.messages}, 400
        except NotUniqueError:
            return {'error': 'Board name already exists'}, 400

    @jwt_required()
    def delete(self, board_id):
        try:
            user_id = get_jwt_identity()
            user = User.objects.get(id=user_id)

            board = Board.objects.get_or_404(id=board_id, owner=user)
            board.delete()
            return {'status': 'success'}, 200
        except OperationError as e:
            return {'errors': 'Operational error'}, 400

boards_view = BoardsAPI.as_view('boards')

blueprint = Blueprint("boards", __name__, url_prefix="/boards")
blueprint.add_url_rule('/', view_func=boards_view, defaults={'board_id': None}, methods=['GET'])
blueprint.add_url_rule('/', view_func=boards_view, defaults={'board_id': None}, methods=['POST'])
blueprint.add_url_rule('/<string:board_id>/cards/', view_func=boards_view, methods=['POST'])
blueprint.add_url_rule('/<string:board_id>', view_func=boards_view, methods=['GET', 'PUT', 'DELETE'])
