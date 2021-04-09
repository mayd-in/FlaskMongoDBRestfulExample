from datetime import datetime
from bson import ObjectId

from flask_bcrypt import generate_password_hash, check_password_hash

from server import db

class User(db.Document):
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True, min_length=6)

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Board(db.Document):
    name = db.StringField(required=True, unique=True)
    status = db.StringField(required=True)
    cards = db.ListField(db.ReferenceField('Card'))
    date_created = db.DateTimeField(default=datetime.utcnow)
    owner = db.ReferenceField(User)
    visible = db.ListField(db.ReferenceField(User))

class Comment(db.EmbeddedDocument):
    id = db.ObjectIdField(required=True, default=lambda: ObjectId())
    text = db.StringField(required=True)
    date_created = db.DateTimeField(default=datetime.utcnow)
    sender = db.ReferenceField(User)

class Card(db.Document):
    title = db.StringField(required=True)
    content = db.ListField(db.EmbeddedDocumentField(Comment))
    start_date = db.DateTimeField()
    end_date = db.DateTimeField()
    date_created = db.DateTimeField(default=datetime.utcnow)
    date_completed = db.DateTimeField()
    owner = db.ReferenceField(User)
    assigned = db.ReferenceField(User)

# User.register_delete_rule(Board, 'owner', db.CASCADE)
# User.register_delete_rule(Board, 'visible', db.CASCADE)