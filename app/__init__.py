
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

db = SQLAlchemy()
load_dotenv()
url = "postgresql://{user}:{passwd}@{host}:{port}/{db}".format(
            user=os.getenv('USER'), passwd=os.getenv('PASSWORD'), host=os.getenv('HOST'), port=os.getenv('PORT'), db=os.getenv('DATABASE')
        )

engine = create_engine(url)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate = Migrate(app, db)
    from .models import Products
    from .views import views
    app.register_blueprint(views,url_prefix='/')
    return app
