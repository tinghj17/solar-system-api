from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os


# creating a new database object 
db = SQLAlchemy()
migrate = Migrate()
load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")

    # connecting db and migrate to our flask 
    db.init_app(app)
    migrate.init_app(app, db)

    # blueprint will response to GET
    from .routes import planets_bp
    app.register_blueprint(planets_bp)

    # this line will respinse to POST
    from app.models.planet import Planet

    return app
