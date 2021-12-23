from flask import (
    request,
    jsonify,
)
from flask_login import logout_user, login_required, current_user, login_user
from werkzeug.security import check_password_hash
from wtforms import ValidationError

from common.errors import not_found, bad_request
from .models import User
from app import db
from . import users


@users.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    try:
        new_user = User(
            lastname=data.get("lastname"),
            firstname=data.get("firstname"),
            email=data.get("email"),
        )
        new_user.set_password(data.get("password"))

        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_json()), 201
    except ValidationError as exception_message:
        db.session.rollback()
        return jsonify(message="Error: {}.".format(exception_message)), 400


@users.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    remember = True if data.get("remember") else False

    if not username or not password:
        return bad_request(
            "Authorization data must be provided",
        )

    user = User.query.filter_by(username=username).first()

    if not user:
        return not_found("No user with such username")

    if check_password_hash(user.password, password):
        login_user(user, remember=remember)
        return jsonify("Logged successfully"), 200

    return bad_request(
        "Incorrect password",
    )


@users.route("/about_user", methods=["GET"])
@login_required
def about_user():
    return jsonify(current_user.to_json()), 200


@users.route("/users", methods=["GET"])
@login_required
def get_users():
    usernames = request.args.getlist("username")

    if usernames:
        users = User.query.filter(User.username.in_(usernames)).all()
    else:
        users = User.query.all()

    return jsonify(User.to_json_list(users))


@users.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return jsonify("Logout successfully"), 200
