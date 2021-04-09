from bson import ObjectId
from marshmallow import fields

from server import ma

ma.Schema.TYPE_MAPPING[ObjectId] = fields.String

class UserSchema(ma.Schema):
    email = fields.Email(required=True)

class BoardSchema(ma.Schema):
    name = fields.Str(required=True)
    cards = fields.Nested('CardSchema', many=True, dump_only=True)
    owner = fields.Nested(UserSchema, dump_only=True, required=True)
    visible_to = fields.Nested(UserSchema, many=True, dump_only=True)

    class Meta:
        additional = ('id', 'status', 'date_created')
        dump_only = ('id', 'date_created')

class CommentSchema(ma.Schema):
    sender = fields.Nested(UserSchema, required=True)

    class Meta:
        additional = ('id', 'text', 'date_created')
        dump_only = ('id', 'date_created')

class CardSchema(ma.Schema):
    content = fields.Nested(CommentSchema, many=True, dump_only=True)
    owner = fields.Nested(UserSchema, required=True)
    assigned = fields.Nested(UserSchema)

    class Meta:
        additional = (
            'id', 'title', 'start_date', 'end_date',
            'date_created', 'date_completed')
        dump_only = ('id', 'owner')
