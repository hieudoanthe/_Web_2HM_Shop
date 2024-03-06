from flask import Blueprint, render_template, flash, request, jsonify, get_flashed_messages
from flask_login import login_required, current_user
from sqlalchemy.sql.functions import user
from .import db
import json
from django.shortcuts import render
from django.db.models import Q
from management.models import Product, Detail, Cart
from urllib.parse import quote
from urllib.parse import quote_plus
from urllib.parse import unquote_plus
from flask_login import user_logged_in

views = Blueprint("views", __name__)

def isLoggedIn():
    # Kiểm tra xem người dùng hiện đã đăng nhập hay chưa
    return current_user.is_authenticated

# Trang chủ
@views.route("/home", methods=["GET","POST"])
@views.route("/", methods=["GET","POST"])
def home(): 
    men_products = []
    women_products = []
    products = Product.query.all()
    for product in products:
        details = Detail.query.filter_by(product_id=product.product_id).all()
        
        for detail in details:
            if detail.type_product == 'Nam_':
                men_products.append((product, detail.type_product))
            elif detail.type_product == 'Nữ_':
                women_products.append((product, detail.type_product))
    first_images = [get_first_image(product.image) for product, _ in men_products]
    first_images += [get_first_image(product.image) for product, _ in women_products]
    messages = get_flashed_messages()
    return render_template("index.html",men_products=men_products, women_products=women_products,first_images=first_images, user=current_user if current_user.is_authenticated else None)
def get_first_image(image):
    # Kiểm tra nếu đường dẫn ảnh không rỗng
    if image:
        # Tách chuỗi đường dẫn ảnh thành một danh sách
        image_list = image.split(';')
        # Trả về tên của ảnh đầu tiên
        return image_list[0]
    # Trả về None nếu không có ảnh nào
    return None


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
@views.route('/infomation/<string:name_product>')
def infomation(name_product):
    decoded_name_product = unquote_plus(name_product)
    product = Product.query.filter_by(name_product=decoded_name_product).first()
    if product:
        detail = Detail.query.filter_by(product_id=product.product_id).first()
        detail.extend = detail.extend.replace('\n','<br>')
        colors = detail.color_product.split(';')
        sizes = detail.size_product.split(';')
        describes = detail.describe.split(';')
        extends = detail.extend.split(';')
        images = product.image.split(';')
        return render_template('info.html', product=product, detail=detail, colors=colors, sizes=sizes, describes=describes, extends=extends, images=images)
    else:
        return name_product

# Cart
def create_cart_for_user(user):
    # Kiểm tra xem người dùng đã có giỏ hàng chưa bằng cách kiểm tra user_id trong bảng Cart
    cart = Cart.query.filter_by(user_id=user.user_id).first()
    if not cart:
        # Nếu không có giỏ hàng cho người dùng này, tạo một giỏ hàng mới
        cart = Cart(user_id=user.user_id)
        db.session.add(cart)
        db.session.commit()

@views.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    # Lấy thông tin sản phẩm từ cơ sở dữ liệu
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Sản phẩm không tồn tại"}), 404

    # Kiểm tra và tạo giỏ hàng cho người dùng nếu cần
    create_cart_for_user(current_user)

    # Lấy giỏ hàng của người dùng
    cart = current_user.cart

    # Thêm sản phẩm vào giỏ hàng
    product.cart_id = cart.cart_id
    db.session.add(product)
    db.session.commit()

    return jsonify({"message": "Thành công"})

# Xử lý sự kiện khi người dùng đăng nhập
@user_logged_in.connect
def on_user_logged_in(sender, user):
    # Kiểm tra và tạo giỏ hàng cho người dùng nếu cần
    create_cart_for_user(user)

@views.route('/cart')
@login_required
def cart():
    # Lấy thông tin giỏ hàng của người dùng hiện tại
    cart = current_user.cart
    if not cart:
        return "Giỏ hàng của bạn đang trống"

    # Lấy danh sách sản phẩm trong giỏ hàng
    products = Product.query.filter_by(cart_id=cart.cart_id).all()

    return render_template('cart.html', products=products)


# Order
@views.route("/order", methods=["GET","POST"])
def order():
    return render_template('order.html')
