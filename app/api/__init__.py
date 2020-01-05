from flask import Blueprint
from flask_restful import Api

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# from . import authentication, posts, users, comments, errors, goals, habits
from . import authentication, habits, users
