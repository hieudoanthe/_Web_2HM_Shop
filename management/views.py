from flask import Blueprint, render_template, flash, request, jsonify, get_flashed_messages
from flask_login import login_required, current_user
from sqlalchemy.sql.functions import user
from .import db
import json
from django.shortcuts import render
from django.db.models import Q
from management.models import Product, Detail

views = Blueprint("views", __name__)

# Trang chủ
@views.route("/home", methods=["GET","POST"])
@views.route("/", methods=["GET","POST"])
def home():
    men_products = []
    women_products = []
    products = Product.query.all()
    for product in products:
        details = Detail.query.filter_by(imei=product.imei).all()
        for detail in details:
            if detail.type_product == 'Nam_':
                men_products.append((product, detail.type_product))
            elif detail.type_product == 'Nữ_':
                women_products.append((product, detail.type_product))
    messages = get_flashed_messages()
    return render_template("index.html",men_products=men_products, women_products=women_products, user=current_user if current_user.is_authenticated else None)

# Nam
@views.route("/male_page", methods=["GET","POST"])
def male_page():
    return render_template('male_page.html')
    # Giày nam
@views.route("/shoemale_page", methods=["GET","POST"])
def shoemale_page():
    return render_template('shoemale_page.html')
@views.route("/fashion_male", methods=["GET","POST"])
    # Thời trang nam
def fashion_male():
    return render_template('fashion_male.html')



# Nữ
@views.route("/female_page", methods=["GET","POST"])
def female_page():
    return render_template('female_page.html')
    # Giày nữ
@views.route("/shoefemale_page", methods=["GET","POST"])
def shoefemale_page():
    return render_template('shoefemale_page.html') 
    # Thời trang nữ
@views.route("/fashion_female", methods=["GET","POST"])
def fashion_female():
    return render_template('fashion_female.html')


    
# Trẻ em
@views.route("/kid_page", methods=["GET","POST"])
def kid_page():
    return render_template('kid_page.html')
    # Giày trẻ em
@views.route("/shoekid_page", methods=["GET","POST"])
def shoekid_page():
    return render_template('shoekid_page.html')
    # Thời trang trẻ em
@views.route("/fashion_kid", methods=["GET","POST"])
def fashion_kid():
    return render_template('fashion_kid.html')



# Infomation
@views.route("/infomation", methods=["GET","POST"])
def infomation():
    return render_template('ifo.html')

# Cart
@views.route("/cart", methods=["GET","POST"])
def cart():
    return render_template('cart.html')

# Order
@views.route("/order", methods=["GET","POST"])
def order():
    return render_template('order.html')