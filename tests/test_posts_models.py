"""
This file contains the unit tests for the posts/models.py file.
"""
import pytest
from wtforms import ValidationError

from posts.models import Post


def test_new_post(new_user):
    post = Post("Test title", "Test description", new_user.uuid)
    assert post.title == "Test title"
    assert post.description == "Test description"
    assert post.puuid == new_user.uuid
    assert post.__repr__() == "<Post: Test title>"


def test_new_post_with_fixture(new_post):
    assert new_post.title == "New title"
    assert new_post.description == "New post description"


def test_new_post_title_exists(new_post, new_user):
    with pytest.raises(ValidationError) as error:
        Post("New title", "Test description", new_user.uuid)

    assert error.value.args[0] == "Title is already in use"


def test_new_post_title_empty(new_user):
    with pytest.raises(ValidationError) as error:
        Post("", "Test description", new_user.uuid)

    assert error.value.args[0] == "Title can not be empty"


def test_new_post_title_incorrect_length(new_user):
    with pytest.raises(ValidationError) as error:
        Post("N", "Test description", new_user.uuid)

    assert error.value.args[0] == "Title must be between 3 and 100 characters"


def test_new_post_description_empty(new_user):
    with pytest.raises(ValidationError) as error:
        Post("New title", "", new_user.uuid)

    assert error.value.args[0] == "Description can not be empty"


def test_new_post_description_incorrect_length(new_user):
    with pytest.raises(ValidationError) as error:
        Post("New title", "Test", new_user.uuid)

    assert error.value.args[0] == "Description must be between 10 and 1000 characters"
