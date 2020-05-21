import logging
from flask import Flask

#  from flask_login import current_user
from celery import Celery

from aivf.blueprints.api import api
from aivf.blueprints.user import user
from aivf.blueprints.page import page
from aivf.blueprints.patient import patient

from aivf.blueprints.user.models import User

from aivf.blueprints.patient.template_processors import bsondate

from aivf.extensions import debug_toolbar, db, login_manager


def create_celery_app(app=None):
    """
    Create a new Celery object and tie together the Celery config to the app's
    config. Wrap all tasks in the context of the application.

    :param app: Flask app
    :return: Celery app
    """
    app = app or create_app()

    celery = Celery(
        app.import_name,
        broker=app.config["CELERY_BROKER_URL"],
        include=CELERY_TASK_LIST,
    )
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


def create_app(settings_override=None):
    """
    Create a Flask application using the app factory pattern

    :return: Flask app
    """
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object("config.settings")
    app.config.from_pyfile("settings.py", silent=True)

    logging_setup(app)

    if settings_override:
        app.config.update(settings_override)

    app.register_blueprint(api, url_prefix="/api")
    app.register_blueprint(user, url_prefix="/user")
    app.register_blueprint(page, url_prefix="/")
    app.register_blueprint(patient, url_prefix="/patient")

    template_processors(app)
    extensions(app)
    authentication(app, User)

    return app


def extensions(app):
    """
    Register extensions by mutating the app argument

    :param app: Flask application instance
    :retrun: None
    """
    db.init_app(app)
    login_manager.init_app(app)
    #  debug_toolbar.init_app(app)

    return None


def authentication(app, user_model):
    """
    Initialize the Flask-Login extension (mutates the app passed in).

    :param app: Flask application instance
    :param User: Model that contains the authentication information
    :type User: Mongoengine model
    :return: None
    """
    login_manager.login_view = "user.login"

    @login_manager.user_loader
    def load_user(uid):
        user = User.objects.exclude("password").get(id=uid)

        if not user.is_active:
            login_manager.login_message = "This account has been disabled."
            return None
        return user


def template_processors(app):
    """
    Register 0 or more custom template processors (mutates the app passed in).

    :param app: Flask application instance
    :return: App jinja environment
    """
    app.jinja_env.filters["bsondate"] = bsondate
    # app.jinja_env.globals.update(current_year=current_year)

    return app.jinja_env


def logging_setup(app):
    logging.basicConfig(level=logging.DEBUG)
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
