from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask.helpers import flash
from sqlalchemy.sql.functions import user
from .models import User, Post
from . import db 
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
 
auth = Blueprint('auth',__name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    posts = Post.query.all()
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user :
            if check_password_hash(user.password, password):
                flash("Logged in!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Wrong password Jose!!!", category='error')
        else:
            flash("Email does not exist!", category='error')

    return render_template('login.html', user= current_user, posts=posts)

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':    
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirmpassword = request.form.get('confirmpassword')

        email_exist = User.query.filter_by(email=email).first()
        username_exist = User.query.filter_by(username=username).first()

        if email_exist:
            flash("This email exist!!!", category='error')
        elif username_exist:
            flash("This username is already in use !!!", category= 'error')
        elif password != confirmpassword:
            flash("Passwords do not match!", category='error')
        elif len(username) < 2:
            flash("Username too short!", category='error')
        elif len(password) < 6:
            flash("Password too short!", category='error')
        elif len(email) < 6 :
            flash("Email too short!", category='error')
        elif ('@' not in email) or ('.' not in email):
            flash("Invalid email!", category='error')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("User created!")
            return redirect(url_for('views.home'))


    return render_template('signup.html', user= current_user)

@login_required
@auth.route('/logout')
def logout():
    logout_user()
    flash("Logged out!", category='success')
    return redirect(url_for('views.home'))
