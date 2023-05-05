import json
from flask import Flask, request, Response
from flask_sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base,sessionmaker
from sqlalchemy import create_engine
import os
import psycopg2

# conn = psycopg2.connect("postgresql://postgres:123456@localhost:5432/postgres")
# url = "postgresql://{user}:{passwd}@{host}:{port}/{db}".format(
#             user=os.environ['USER'], passwd=os.environ['PASSWORD'], host=os.environ['HOST'], port=os.environ['PORT'], db=os.environ['DATABASE']
#         )

url = "postgresql://postgres:123456@localhost:5432/test"
app = Flask(__name__)


Base = declarative_base()

class Products(Base):
    __tablename__ = 'products'
    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(250),nullable=False)

engine = create_engine(url)
Base.metadata.create_all(engine)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

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

@app.route('/create',methods = 'POST')
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
app.run()