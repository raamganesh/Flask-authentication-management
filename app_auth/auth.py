from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .data_model import User
from flask_login import login_user, login_required, logout_user
from . import db

auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    """Render template for login page
    """
    return render_template("login.html")


@auth.route("/login", methods=["POST"])
def login_post():
    """POST method to get input data from customer for authentication
    """
    # Get required data from the form
    email = request.form.get("email")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    # Check for duplication
    user = User.query.filter_by(email=email).first()

    # Notify customer if the authentication step is fail
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login detail and try again.')
        return redirect(url_for("auth.login"))

    # Authentication step is successful, redirect to the user's profile page
    login_user(user, remember=remember)
    return redirect(url_for("main.profile"))


@auth.route("/signup")
def signup():
    """Render tamplate for sign up page
    """
    return render_template("signup.html")


@auth.route("/signup", methods=["POST"])
def signup_post():
    """POST method to get customer's information from the form to check for duplication
    and sign up
    """
    # Get required data from the form
    email = request.form.get("email")
    name = request.form.get("name")
    password = request.form.get("password")

    # Check for duplication
    user = User.query.filter_by(email=email).first()

    # Notify customer if the email is already registered
    if user:
        flash("Email already exists")
        return redirect(url_for("auth.signup"))

    # Register customer information into the system
    new_user = User(email=email,
                    name=name,
                    password=generate_password_hash(password, method="sha256"))

    db.session.add(new_user)
    db.session.commit()

    # Redirect to the login page
    return redirect(url_for("auth.login"))


@auth.route("/logout")
@login_required
def logout():
    """Redirect customer to index page after signing out
    """
    logout_user()
    return redirect(url_for("main.index"))