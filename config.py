import os


class BaseConfiguration:
    DEBUG = True
    TESTING = False
    SECRET_KEY = "hello-world"
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DEV_DATABASE_URL")
        or "postgresql://postgres:postgres@localhost:5432/test_database"
    )


class TestConfiguration(BaseConfiguration):
    TESTING = True
    WTF_CSRF_ENABLED = False
    DEBUG = False

    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL") or (
        "postgresql://postgres:postgres@localhost:5432/testdatabase"
    )
