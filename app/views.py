import json
from flask import Blueprint, Response, request

from .models import Products
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from config import Config 
views = Blueprint('views',__name__)

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

@views.route("/")
def index():
    return "Hello"

@views.route('/products')
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

@views.route('/create',methods = ['POST'])
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
