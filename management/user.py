from re import template
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, get_flashed_messages
from sqlalchemy.sql.expression import false
from management.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from management import db
from sqlalchemy import or_


user = Blueprint("user", __name__)

@user.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password, password):
                session.permanent = True
                login_user(user,remember=True)
                flash("Logged is success !",category="success")
                return redirect(url_for("views.home"))
            else:
                flash("Password is wrong :)",category="error")
        else:
            flash("User doesn't exist !",category="error")
    messages = get_flashed_messages()
    return render_template("login.html", user = current_user)

@user.route("/signup",methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        data = request.form.get("data")
        phone_number = request.form.get("email")
        user_name = request.form.get("user_name")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        # Kiểm tra xem dữ liệu là email hay số điện thoại
        if data.isdigit():
            phone_number = data
            email = None
        else:
            email = data
            phone_number = None

        user = User.query.filter(or_(User.email == email, User.phone_number == phone_number)).first()
        if user:
            flash("User existed !", category="error")
        elif len(email) < 4:
            flash("Email sort !", category="error")
        elif len(password) < 7:
            flash("Password sort !",category="error")
        elif password != confirm_password:
            flash("Password does not match !",category="error")
        else:  
            password = generate_password_hash(password, method="sha256")
            new_user = User(email=email, phone_number = phone_number, password=password, user_name=user_name)
            try:
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user,remember=True)
                flash("User created !", category="success")
                return redirect(url_for("views.home"))   
            except:
                "error"
    messages = get_flashed_messages()
    return render_template("signup.html", user=current_user)

@user.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("user.login"))