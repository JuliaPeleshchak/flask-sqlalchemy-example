from flask import Blueprint

posts = Blueprint("posts", __name__)


from posts import models
from posts import views
