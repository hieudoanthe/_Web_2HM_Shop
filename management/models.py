from management import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import DECIMAL
from sqlalchemy.orm import relationship
from datetime import datetime 
from sqlalchemy import LargeBinary

class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)

    user_name = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.Integer)
    registration_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    orders = db.relationship('Order', backref='user', lazy=True)
    carts = db.relationship('Cart', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Order(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    email = db.Column(db.String(30))
    phone_number = db.Column(db.Integer)
    address = db.Column(db.String(40))
    city = db.Column(db.String(20))
    state = db.Column(db.String(20))
    zip_code = db.Column(db.Integer)

    def __repr__(self):
        return f"Order('{self.user_id}')"

class Cart(db.Model):
    cart_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    imei = db.Column(db.String(36), nullable=False, unique=True)

    products = db.relationship('Product', backref='user', lazy=True)

    def __init__(self, *args, **kwargs):
            super(Cart, self).__init__(*args, **kwargs)
            self.imei = str(uuid.uuid4())

    def __repr__(self):
        return f"Cart('{self.cart_id}', '{self.user_id}', '{self.imei}')"

class Product(db.Model):
    imei = db.Column(db.String(36), db.ForeignKey('cart.imei'), primary_key=True)

    name_product = db.Column(db.String(200))
    price = db.Column(db.DECIMAL(precision=12, scale=2)) 
    quantity = db.Column(db.Integer)
    image = db.Column(db.String(255))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    details = db.relationship('Detail', backref='user', lazy=True)

class Detail(db.Model):
    imei = db.Column(db.String(36), db.ForeignKey('product.imei'), primary_key=True)
    type_product = db.Column(db.String(255))
    color_product = db.Column(db.String(20))
    size_product = db.Column(db.String(5))
    producer = db.Column(db.String(255))

class Income(db.Model):
    income_id = db.Column(db.Integer, primary_key=True)
    total_price = db.Column(db.Float, nullable=False)