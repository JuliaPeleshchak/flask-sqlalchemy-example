import datetime
import re
import uuid
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash
from wtforms import ValidationError

from app import db


class User(db.Model):
    __tablename__ = "users"

    uuid = db.Column(db.String(500), primary_key=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    username = db.Column(db.String(50), unique=True, index=True)
    password = db.Column(db.String(500))
    email = db.Column(db.String(50), unique=True, index=True)
    dateofreg = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, firstname, lastname, email):
        self.firstname = firstname
        self.lastname = lastname
        self.username = email
        self.email = email
        self.uuid = str(uuid.uuid4())

    def __repr__(self):
        return f"<User: {self.email}>"

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.uuid)

    def to_json(self):
        return {
            "uuid": self.uuid,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "username": self.username,
            "email": self.email,
            "password": self.password,
        }

    @staticmethod
    def to_json_list(users):
        return [user.to_json() for user in users]

    @validates("email")
    def validate_email(self, key, email):
        if not email:
            raise ValidationError("Email can not be empty")
        if not re.match("[^@]+@[^@]+\.[^@]+", email):
            raise ValidationError("Provided email is not correct email address")
        if User.query.filter_by(email=email).first():
            raise ValidationError("Email is already in use")

        return email

    @validates("firstname")
    def validate_firstname(self, key, firstname):
        if not firstname:
            raise ValidationError("Firstname can not be empty")
        return firstname

    @validates("lastname")
    def validate_lastname(self, key, lastname):
        if not lastname:
            raise ValidationError("Lastname can not be empty")
        return lastname

    def set_password(self, password):
        if not password:
            raise ValidationError("Password can not be empty")
        if not re.match("\d.*[A-Z]|[A-Z].*\d", password):
            raise ValidationError("Password must contain 1 capital letter and 1 number")
        if len(password) < 8 or len(password) > 50:
            raise ValidationError("Password must be between 8 and 50 characters")
        self.password = generate_password_hash(password)
