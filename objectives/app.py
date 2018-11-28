from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from objectives.database import db
from objectives.views import blueprints


def create_app():
    app = Flask(__name__)

    app.config['WTF_CSRF_SECRET_KEY'] = 'A SECRET KEY'
    app.config['SECRET_KEY'] = 'ANOTHER ONE'

    # Database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///objectives.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Register blueprints
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
        blueprint.app = app

    # Init database
    db.init_app(app)
    db.create_all(app=app)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0", port=5004, debug=True)
