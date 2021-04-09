from flask import Blueprint, request, Response
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from server import db, ma
from server.database.models import User, Comment
from server.database.schemas import CommentSchema


class CommentsAPI(MethodView):
    def get(self, comment_id):
        comment = Comment.objects.get_or_404(id=comment_id)
        resp = CommentSchema().dumps(comment)
        return Response(resp, mimetype="application/json", status=200)

    @jwt_required()
    def put(self, comment_id):
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)
        comment = Comment.objects.get_or_404(id=comment_id, owner=user)

        data = request.get_json(force=True)
        comment.update(**data)
        comment.save()
        return {'status': 'success'}, 200

    @jwt_required()
    def delete(self, comment_id):
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)
        comment = Comment.objects.get_or_404(id=comment_id, owner=user)
        comment.delete()
        return {'status': 'success'}, 200

comments_view = CommentsAPI.as_view('comments')

blueprint = Blueprint("comments", __name__, url_prefix="/comments")
blueprint.add_url_rule('/<string:card_id>', view_func=comments_view, methods=['GET', 'PUT', 'DELETE'])
