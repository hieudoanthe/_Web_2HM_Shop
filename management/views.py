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

# Nữ
@views.route("/female_page", methods=["GET","POST"])
def female_page():
    return render_template('female_page.html')

# Trẻ em
@views.route("/kid_page", methods=["GET","POST"])
def kid_page():
    return render_template('kid_page.html')
