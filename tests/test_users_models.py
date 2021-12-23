"""
This file contains the unit tests for the users/models.py file.
"""
import pytest
from werkzeug.security import check_password_hash
from wtforms import ValidationError

from users.models import User


def test_new_user():
    user = User(firstname="Joe", lastname="Duo", email="joe.duo@gmail.com")
    user.set_password("Test1234")
    assert user.email == "joe.duo@gmail.com"
    assert check_password_hash(user.password, "Test1234")
    assert user.firstname == "Joe"
    assert user.lastname == "Duo"
    assert user.username == "joe.duo@gmail.com"
    assert user.__repr__() == "<User: joe.duo@gmail.com>"
    assert user.is_authenticated
    assert user.is_active


def test_new_user_with_fixture(new_user):
    assert new_user.email == "joe.duo@gmail.com"
    assert check_password_hash(new_user.password, "Test1234")
    assert new_user.firstname == "Joe"
    assert new_user.lastname == "Duo"
    assert new_user.username == "joe.duo@gmail.com"


def test_setting_password(new_user):
    new_user.set_password("MyNewPassword1")
    assert check_password_hash(new_user.password, "MyNewPassword1")
    assert not check_password_hash(new_user.password, "MyNewPassword2")


def test_new_user_no_firstname():
    with pytest.raises(ValidationError) as error:
        user = User(firstname=None, lastname="Duo", email="joe.duo@gmail.com")
        user.set_password("Test1234")

    assert error.value.args[0] == "Firstname can not be empty"


def test_new_user_no_lastame():
    with pytest.raises(ValidationError) as error:
        user = User(firstname="Joe", lastname="", email="joe.duo@gmail.com")
        user.set_password("Test1234")

    assert error.value.args[0] == "Lastname can not be empty"


def test_new_user_no_email():
    with pytest.raises(ValidationError) as error:
        user = User(firstname="Joe", lastname="Duo", email="")
        user.set_password("Test1234")

    assert error.value.args[0] == "Email can not be empty"


def test_new_user_incorrect_email():
    with pytest.raises(ValidationError) as error:
        user = User(firstname="Joe", lastname="Duo", email="joe.duogmail.com")
        user.set_password("Test1234")

    assert error.value.args[0] == "Provided email is not correct email address"


def test_new_user_already_exists_email(new_user):
    with pytest.raises(ValidationError) as error:
        user = User(firstname="Joe", lastname="Duo", email="joe.duo@gmail.com")
        user.set_password("Test1234")

    assert error.value.args[0] == "Email is already in use"


def test_setting_password_no_password(new_user):
    with pytest.raises(ValidationError) as error:
        new_user.set_password("")

    assert error.value.args[0] == "Password can not be empty"


def test_setting_password_not_strong(new_user):
    with pytest.raises(ValidationError) as error:
        new_user.set_password("testpassword")

    assert error.value.args[0] == "Password must contain 1 capital letter and 1 number"


def test_setting_password_short_password(new_user):
    with pytest.raises(ValidationError) as error:
        new_user.set_password("Test11")

    assert error.value.args[0] == "Password must be between 8 and 50 characters"
