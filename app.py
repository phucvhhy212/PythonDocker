from flask import Flask
import psycopg2
conn = psycopg2.connect("postgresql://postgres:123456@localhost:5432/postgres")
app = Flask(__name__)
# Define root router
@app.route('/')
def hello_world():
    return 'Hello, Worlds !!!'
@app.route('/product')
def getProducts():
    return 'Hello, Worlds !!!'


