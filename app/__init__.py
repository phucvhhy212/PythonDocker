
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

db = SQLAlchemy()


engine = create_engine(os.environ.get('SQLALCHEMY_DATABASE_URI'))
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevConfig')
    db.init_app(app)
    migrate = Migrate(app, db)
    from .models import Products
    from .views import views
    app.register_blueprint(views,url_prefix='/')
    return app
