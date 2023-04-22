import json
from flask import Flask, render_template, request, url_for, redirect
import os
import psycopg2

# conn = psycopg2.connect("postgresql://postgres:123456@localhost:5432/postgres")
url = "postgresql://{user}:{passwd}@{host}:{port}/{db}".format(
            user=os.environ['USER'], passwd=os.environ['PASSWORD'], host=os.environ['HOST'], port=os.environ['PORT'], db=os.environ['DATABASE']
        )

# url = "postgresql://postgres:123456@localhost:5432/postgres"
app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(url)
    return conn


@app.route('/initdb')
def inittable():
    conn = psycopg2.connect(url)
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS products;')
    cur.execute('CREATE TABLE products(id INT PRIMARY KEY,name VARCHAR(50));')
    cur.execute("INSERT INTO products(id,name) VALUES('1','Laptop')")
    cur.execute("INSERT INTO products(id,name) VALUES('2','TV')")
    conn.commit()
    cur.close()
    conn.close()
    return "initialized ! "


@app.route('/products')
def getProducts():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM PRODUCTS;')
    row_headers = [x[0] for x in cur.description] #('id','name')

    
    products = cur.fetchall()
    for product in products: #(1,'Laptop')
        print(product)
    json_data = []
    #zip: [(id,1),(name,Laptop)]
    # to dictionary: [{id:1,name:"Laptop"}]
    # smt dictionary == json
    for product in products:
        json_data.append(dict(zip(row_headers,product)))
    cur.close()
    conn.close()
    return json.dumps(json_data) #convert to JSOn

@app.route('/create',methods = ['POST', 'GET'])
def create():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO products(id,name)'
                    'VALUES (%s, %s)',
                    (id,name))
        conn.commit()
        cur.close()
        conn.close()
        return redirect('../products',302)

    return render_template('create.html')