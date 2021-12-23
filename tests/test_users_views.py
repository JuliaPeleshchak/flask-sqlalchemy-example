"""
This file contains the unit tests for the users/views.py file.
"""
import json

import app
from common.errors import bad_request, not_found
from users.models import User


def test_signup(test_client, delete_db_data):
    firstname = "Alex"
    lastname = "Melon"
    email = "alex.melon@gmail.com"
    password = "Test12345"

    response = test_client.post(
        "/signup",
        data=json.dumps(
            dict(firstname=firstname, lastname=lastname, email=email, password=password)
        ),
        content_type="application/json",
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["firstname"] == firstname
    assert data["lastname"] == lastname
    assert data["email"] == email
    assert data["username"] == email
    assert "uuid" in data
    assert "password" in data

    app.db.session.delete(User.query.get_or_404(data["uuid"]))
    app.db.session.commit()


def test_signup_no_firstname(test_client, delete_db_data):
    lastname = "Melon"
    email = "alex.melon@gmail.com"
    password = "Test12345"

    response = test_client.post(
        "/signup",
        data=json.dumps(
            dict(firstname="", lastname=lastname, email=email, password=password)
        ),
        content_type="application/json",
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data == {"message": "Error: Firstname can not be empty."}


def test_login(test_client, new_user, delete_db_data):
    response = test_client.post(
        "/login",
        data=json.dumps(dict(username=new_user.username, password="Test1234")),
        content_type="application/json",
    )
    assert response.status_code == 200
    assert b"Logged successfully" in response.data


def test_login_empty_username(test_client, delete_db_data):
    response = test_client.post(
        "/login",
        data=json.dumps(dict(username="", password="Test1234")),
        content_type="application/json",
    )
    assert response.status_code == 400
    assert (
        response.data
        == bad_request(
            "Authorization data must be provided",
        ).data
    )


def test_login_no_such_user(test_client, delete_db_data):
    response = test_client.post(
        "/login",
        data=json.dumps(dict(username="test@gmail.com", password="Test1234")),
        content_type="application/json",
    )
    assert response.status_code == 404
    assert response.data == not_found("No user with such username").data


def test_login_incorrect_password(test_client, new_user, delete_db_data):
    response = test_client.post(
        "/login",
        data=json.dumps(dict(username=new_user.username, password="Test123456")),
        content_type="application/json",
    )
    assert response.status_code == 400
    assert (
        response.data
        == bad_request(
            "Incorrect password",
        ).data
    )


def test_about_user(test_client, logged_user, delete_db_data):
    response = test_client.get("/about_user")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data == logged_user.to_json()


def test_get_users(test_client, logged_user, delete_db_data):
    user1 = User("Joe1", "Duo1", "joe1.duo1@gmail.com")
    user1.set_password("Joe1duo1")
    user2 = User("Joe2", "Duo2", "joe2.duo2@gmail.com")
    user2.set_password("Joe2duo2")
    app.db.session.add(user1)
    app.db.session.add(user2)

    response = test_client.get("/users")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 3
    assert user1.to_json() in data
    assert user2.to_json() in data
    assert logged_user.to_json() in data


def test_get_users_by_username(test_client, delete_db_data):
    user1 = User("Joe1", "Duo1", "joe1.duo1@gmail.com")
    user1.set_password("Joe1duo1")
    user2 = User("Joe2", "Duo2", "joe2.duo2@gmail.com")
    user2.set_password("Joe2duo2")
    app.db.session.add(user1)
    app.db.session.add(user2)

    response = test_client.get("/users?username=joe1.duo1@gmail.com")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert user1.to_json() in data
    assert user2.to_json() not in data


def test_logout(test_client, delete_db_data):
    response = test_client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert b"Logout successfully" in response.data
