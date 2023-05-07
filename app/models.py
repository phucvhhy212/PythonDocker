from . import db


class Products(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(250),nullable=False)
