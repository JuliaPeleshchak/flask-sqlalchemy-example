from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


login_manager = LoginManager()
db = SQLAlchemy()


def create_app(config_name="config.BaseConfiguration"):
    app = Flask(__name__)
    app.config.from_object(config_name)
    init_db(app)
    register_blueprints(app)
    add_login_manager(app)
    return app


def init_db(app):
    db.init_app(app)
    Migrate(app, db, compare_type=True)


def register_blueprints(app):
    from users import users as users_blueprint
    from posts import posts as posts_blueprint

    app.register_blueprint(users_blueprint)
    app.register_blueprint(posts_blueprint)


def add_login_manager(app):
    login_manager.init_app(app)
    login_manager.login_message = "You Must Login to Access This Page!"

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    from users.models import User

    @login_manager.user_loader
    def load_user(user_uuid):
        return User.query.get(str(user_uuid))


if __name__ == "__main__":
    app = create_app("config.BaseConfiguration")
    app.run(debug=True)
