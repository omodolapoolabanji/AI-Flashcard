from application import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Document):
    user_id = db.IntField(unique=True)
    username = db.StringField(max_length=20)

    email = db.StringField(max_length=30, unique=True)
    password = db.StringField()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Flashcards(db.Document):
    flashcard_id = db.IntField(unique=True)
    question = db.StringField(max_length=700)
    answer = db.StringField(max_length=700)
    user_id = db.IntField()
