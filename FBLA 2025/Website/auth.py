from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from Website import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        FirstName = request.form.get('FirstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user_type = request.form.get('UserType')
        business_name = request.form.get('BusinessName') if user_type == 'BusinessOwner' else None

        user = User.query.filter_by(email=email).first()

        if user:
            flash('This user already exists', category='error')
        elif len(email) < 4:
            flash('Email must be more than 3 characters', category='error')
        elif len(FirstName) < 2:
            flash('First name must be longer than 1 character', category='error')
        elif password1 != password2:
            flash('Passwords do not match', category='error')
        elif len(password1) < 7:
            flash('Password needs to be longer', category='error')
        else:
            # Hash the password and create the new user
            hashed_pw = generate_password_hash(password1, method='pbkdf2:sha256')
            new_user = User(
                email=email,
                FirstName=FirstName,
                password=hashed_pw,
                user_type='business' if user_type == 'BusinessOwner' else 'customer'
            )
            db.session.add(new_user)
            db.session.commit()

            # Automatically create a Business entry if the user is a Business Owner
            if user_type == 'BusinessOwner' and business_name:
                from .models import Business
                new_business = Business(
                    biz_name=business_name,
                    category='Uncategorized',  # You can replace this later with form data
                    user_id=new_user.id
                )
                db.session.add(new_business)
                db.session.commit()

            flash('Account creation successful!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password1')
        user = User.query.filter_by(email=email).first()
    
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect email or password, try again', category='error')
        else:
            flash('No user found or account is misconfigured.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
