import json
from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv


load_dotenv()

url = "postgresql://{user}:{passwd}@{host}:{port}/{db}".format(
            user=os.getenv('USER'), passwd=os.getenv('PASSWORD'), host=os.getenv('HOST'), port=os.getenv('PORT'), db=os.getenv('DATABASE')
        )
# url = "postgresql://postgres:123456@postgres:5432/test"
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app,db)


class Products(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(250),nullable=False)

engine = create_engine(url)

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

@app.route("/")
def index():
    return "Hello"

@app.route('/products')
def getProducts():
    products = session.query(Products).all()
    json_data = []
    # row_headers = [x[0] for x in cur.description] #('id','name')
    row_headers =  [column.key for column in Products.__table__.columns]
    #zip: [(id,1),(name,Laptop)]
    # to dictionary: [{id:1,name:"Laptop"}]
    # smt dictionary == json
    for product in products:
        json_data.append(dict(zip(row_headers,[product.id,product.name])))
    
    resp = Response(json.dumps(json_data),200,mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/create',methods = ['POST'])
def create():
    row_headers =  [column.key for column in Products.__table__.columns]
    json_data = []
    pname = request.form['name']
    product = Products(name=pname)
    session.add(product)
    session.commit()
    json_data.append(dict(zip(row_headers,[product.id,product.name])))
    resp = Response(json.dumps(json_data),200,mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
