"""
This file contains the unit tests for the posts/views.py file.
"""
import json

import app
from common.errors import forbidden
from posts.models import Post


def test_show_posts(test_client, logged_user, delete_db_data):
    post1 = Post("New title1", "New post1 description", logged_user.uuid)
    app.db.session.add(post1)

    post2 = Post("New title2", "New post2 description", logged_user.uuid)
    app.db.session.add(post2)

    response = test_client.get("/posts")

    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 2
    assert post1.to_json() in data
    assert post2.to_json() in data


def test_show_posts_by_id(test_client, logged_user, delete_db_data):
    post1 = Post("New title1", "New post1 description", logged_user.uuid)
    app.db.session.add(post1)

    post2 = Post("New title2", "New post2 description", logged_user.uuid)
    app.db.session.add(post2)

    response = test_client.get(f"/posts?id={post1.pid}")

    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert post1.to_json() in data
    assert post2.to_json() not in data


def test_add_post(test_client, logged_user, delete_db_data):
    title = "New title"
    description = "New post description"
    response = test_client.post(
        f"/posts",
        data=json.dumps(dict(title=title, description=description)),
        content_type="application/json",
    )

    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["title"] == title
    assert data["description"] == description
    assert data["user_uuid"] == logged_user.uuid
    assert "id" in data


def test_add_post_empty_title(test_client, logged_user, delete_db_data):
    description = "New post description"
    response = test_client.post(
        f"/posts",
        data=json.dumps(dict(title="", description=description)),
        content_type="application/json",
    )

    assert response.status_code == 400
    data = json.loads(response.data)
    assert data == {"message": "Error: Title can not be empty."}


def test_delete_post(test_client, logged_user, delete_db_data):
    post = Post("New title1", "New post1 description", logged_user.uuid)
    app.db.session.add(post)
    app.db.session.commit()

    response = test_client.delete(f"/posts/{post.pid}")

    assert response.status_code == 200
    assert b"Post was successfully deleted" in response.data


def test_delete_post_forbidden(test_client, new_user, delete_db_data):
    post = Post("New title1", "New post1 description", new_user.uuid)
    app.db.session.add(post)
    app.db.session.commit()

    response = test_client.delete(f"/posts/{post.pid}")

    assert response.status_code == 403
    assert response.data == forbidden("You can not delete this post").data

    app.db.session.delete(post)
    app.db.session.delete(new_user)
    app.db.session.commit()


def test_update_post(test_client, logged_user, delete_db_data):
    post = Post("New title1", "New post1 description", logged_user.uuid)
    app.db.session.add(post)
    app.db.session.commit()

    assert post.title == "New title1"

    response = test_client.put(
        f"/posts/{post.pid}",
        data=json.dumps(
            dict(
                title="New title2",
            )
        ),
        content_type="application/json",
    )

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data == post.to_json()
    assert post.title == "New title2"

    app.db.session.delete(post)
    app.db.session.commit()


def test_update_post_incorrect_title(test_client, logged_user, delete_db_data):
    post = Post("New title1", "New post1 description", logged_user.uuid)
    app.db.session.add(post)
    app.db.session.commit()

    response = test_client.put(
        f"/posts/{post.pid}",
        data=json.dumps(
            dict(
                title="N",
            )
        ),
        content_type="application/json",
    )

    assert response.status_code == 400
    data = json.loads(response.data)
    assert data == {"message": "Error: Title must be between 3 and 100 characters."}

    app.db.session.delete(post)
    app.db.session.commit()


def test_update_post_forbidden(test_client, new_user, delete_db_data):
    post = Post("New title1", "New post1 description", new_user.uuid)
    app.db.session.add(post)
    app.db.session.commit()

    response = test_client.put(
        f"/posts/{post.pid}",
        data=json.dumps(
            dict(
                title="New",
            )
        ),
        content_type="application/json",
    )

    assert response.status_code == 403
    assert response.data == forbidden("You can not update this post").data

    app.db.session.delete(post)
    app.db.session.delete(new_user)
    app.db.session.commit()
