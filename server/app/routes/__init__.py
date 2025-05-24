from flask import Blueprint
from .tags import tags_bp
from .calls import calls_bp
from .tasks import tasks_bp
from .users import users_bp
from .auth import auth_bp

def register_routes(app):
    app.register_blueprint(tags_bp, url_prefix='/api/tags')
    app.register_blueprint(calls_bp, url_prefix='/api/calls')
    app.register_blueprint(tasks_bp, url_prefix='/api/tasks')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(auth_bp, url_prefix='/api')
