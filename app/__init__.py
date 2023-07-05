
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevConfig')
    db.init_app(app)
    migrate = Migrate(app, db)
    from .models import Products
    from .views import views
    app.register_blueprint(views,url_prefix='/')
    return app
