import flask_migrate
import pytest

from app import create_app, db
from posts.models import Post
from users.models import User
import app


@pytest.fixture(scope="function", autouse=True)
def delete_db_data():
    yield
    db.session.remove()


@pytest.fixture(scope="session", autouse=True)
def test_client():
    flask_app = create_app("config.TestConfiguration")

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            flask_migrate.upgrade()
            db.create_all()
            try:
                yield testing_client
            finally:
                db.drop_all()


@pytest.fixture(scope="function")
def new_user():
    user = User("Joe", "Duo", "joe.duo@gmail.com")
    user.set_password("Test1234")
    db.session.add(user)
    return user


@pytest.fixture(scope="session")
def logged_user():
    user = User("User", "Logged", "user.logged@gmail.com")
    user.set_password("Test1234")
    db.session.add(user)
    db.session.commit()

    @app.login_manager.request_loader
    def load_user_from_request(request):
        return user

    return user


@pytest.fixture(scope="function")
def new_post():
    user = User("Jon", "Duo", "jon.duo@gmail.com")
    user.set_password("Test1234")
    db.session.add(user)
    post = Post("New title", "New post description", user.uuid)
    db.session.add(post)
    return post
