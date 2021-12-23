from sqlalchemy.orm import validates
from wtforms import ValidationError

from app import db


class Post(db.Model):
    __tablename__ = "posts"

    pid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(1000))
    puuid = db.Column(db.String, db.ForeignKey("users.uuid"))

    user = db.relationship("User", backref=db.backref("posts", lazy=True))

    def __init__(self, title, description, puuid):
        self.title = title
        self.description = description
        self.puuid = puuid

    def __repr__(self):
        return f"<Post: {self.title}>"

    def to_json(self):
        return {
            "id": self.pid,
            "title": self.title,
            "description": self.description,
            "user_uuid": self.puuid,
        }

    @staticmethod
    def to_json_list(posts):
        return [post.to_json() for post in posts]

    @validates("title")
    def validate_title(self, key, title):
        if not title:
            raise ValidationError("Title can not be empty")

        if Post.query.filter_by(title=title).first():
            raise ValidationError("Title is already in use")

        if len(title) < 3 or len(title) > 100:
            raise ValidationError("Title must be between 3 and 100 characters")
        return title

    @validates("description")
    def validate_description(self, key, description):
        if not description:
            raise ValidationError("Description can not be empty")

        if len(description) < 10 or len(description) > 100:
            raise ValidationError("Description must be between 10 and 1000 characters")
        return description
