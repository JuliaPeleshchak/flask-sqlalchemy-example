from flask import (
    request,
    jsonify,
)
from flask_login import login_required, current_user
from wtforms import ValidationError

from app import db
from common.errors import forbidden
from posts.models import Post
from . import posts


@posts.route("/posts", methods=["GET"])
@login_required
def show_posts():
    post_ids = request.args.getlist("id")
    if post_ids:
        posts = Post.query.filter(Post.pid.in_(post_ids)).all()
    else:
        posts = Post.query.all()

    return jsonify(Post.to_json_list(posts)), 200


@posts.route("/posts", methods=["POST"])
@login_required
def add_post():
    data = request.get_json()

    try:
        post = Post(
            title=data.get("title"),
            description=data.get("description"),
            puuid=current_user.uuid,
        )
        db.session.add(post)
        db.session.commit()
        return jsonify(post.to_json()), 201
    except ValidationError as exception_message:
        db.session.rollback()
        return jsonify(message="Error: {}.".format(exception_message)), 400


@posts.route("/posts/<id>", methods=["DELETE"])
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    if current_user.uuid != post.user.uuid:
        return forbidden("You can not delete this post")

    db.session.delete(post)
    db.session.commit()
    return jsonify("Post was successfully deleted"), 200


@posts.route("/posts/<id>", methods=["PUT"])
@login_required
def update_post(id):
    post = Post.query.get_or_404(id)
    if current_user.uuid != post.user.uuid:
        return forbidden("You can not update this post")
    data = request.get_json()
    try:
        post.title = data.get("title", post.title)
        post.description = data.get("description", post.description)
        db.session.commit()
    except ValidationError as exception_message:
        db.session.rollback()
        return jsonify(message="Error: {}.".format(exception_message)), 400

    return jsonify(post.to_json()), 200
