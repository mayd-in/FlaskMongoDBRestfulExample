from bson import ObjectId
from marshmallow import fields, validate

from server import ma

ma.Schema.TYPE_MAPPING[ObjectId] = fields.String

class UserSchema(ma.Schema):
    id = fields.String(dump_only=True)
    email = fields.Email(required=True, validate=validate.Length(max=64))
    password = fields.String(required=True, load_only=True, validate=validate.Length(min=6, max=64))

    class Meta:
        ordered = True

class BoardSchema(ma.Schema):
    name = fields.String(required=True)
    status = fields.String(required=True, validate=validate.OneOf(["active", "archived"]))
    cards = fields.Nested('CardSchema', many=True, dump_only=True)
    owner = fields.Nested(UserSchema, required=True, dump_only=True)
    visible_to = fields.Nested(UserSchema, many=True, dump_only=True)

    class Meta:
        ordered = True
        additional = ('id', 'date_created')
        dump_only = ('id', 'date_created')

class CommentSchema(ma.Schema):
    text = fields.String(required=True)
    sender = fields.Nested(UserSchema, dump_only=True)

    class Meta:
        additional = ('id', 'date_created')
        dump_only = ('id', 'date_created')

class CardSchema(ma.Schema):
    title = fields.String(required=True)
    content = fields.Nested(CommentSchema, many=True, dump_only=True)
    start_date = fields.DateTime()
    end_date = fields.DateTime()
    date_completed = fields.DateTime()
    owner = fields.Nested(UserSchema, dump_only=True)
    assigned = fields.Nested(UserSchema)

    class Meta:
        ordered = True
        additional = ('id', 'date_created')
        dump_only = ('id', 'date_created')
