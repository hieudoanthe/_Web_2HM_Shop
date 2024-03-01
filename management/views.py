from flask import Blueprint, render_template, flash, request, jsonify, get_flashed_messages
from flask_login import login_required, current_user
from sqlalchemy.sql.functions import user
from .import db
import json
from django.shortcuts import render
from django.db.models import Q

views = Blueprint("views", __name__)

# Trang chủ
@views.route("/home", methods=["GET","POST"])
@views.route("/", methods=["GET","POST"])
def home():
    if request.method == "POST":
        note = request.form.get("note")
        if len(note) < 1:
            flash("Note sort:)",category="error")
        else:
            new_note = Note(data = note, user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added !",category="success")
    messages = get_flashed_messages()
    return render_template("index.html", user=current_user if current_user.is_authenticated else None)

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
