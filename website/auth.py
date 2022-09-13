from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, NursingHome
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_type = request.form.get('login-type') # Staff/User is "login" while Guest is "login-guest"
        
        # Staff/User
        if login_type == "login":
            email = request.form.get('email')
            password = request.form.get('password')
            
            staff_admin = NursingHome.query.filter_by(email=email).first()
            if staff_admin:
                # if check_password_hash(user.password, password):
                if staff_admin.password == password:
                    # flash('Logged in successfully!', category='success')
                    login_user(staff_admin, remember=True)
                    return redirect(url_for('views.home'))
                else:
                    flash('Incorrect password, try again.', category='error')
            else:
                flash('Email does not exist.', category='error')
        # Guest
        elif login_type == "login-guest":
            nursing_home_ID = request.form.get('homeId')
            
            guest = NursingHome.query.filter_by(id=nursing_home_ID).first()
            if guest:
                login_user(guest, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Wrong Nursing Home ID', category='error')
        else:
            flash('Something went wrong, could not find the right login form', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# TODO: Needs some clean up and the front end as well, need to decide which input labels to record/keep
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        # Default activity and wellbeing list
        activity_list = "bowling,tennis,golf,bike,tea,chess"
        wellbeing_list = "neutral,very-sad,happy,sick,sad,angry"
        
        # Creates the one admin profile for each nursing home
        nursing_home_name = request.form.get('nursing-home-name')
        nursing_home_id = request.form.get('homeId')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        agreeCheck = request.form.get('agreeCheck')

        # Look up email and nursing home name to see if they exist in the database already
        existing_nursing_home_admin_email = User.query.filter_by(email=email).first()
        existing_nursing_home_name = NursingHome.query.filter_by(name=nursing_home_name).first()
        if existing_nursing_home_admin_email:
            flash('Email already exists.', category='error')
        elif existing_nursing_home_name:
            flash('Nursing Home Name already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 6:
            flash('Password must be at least 6 characters.', category='error')
        elif not nursing_home_id.isdigit():
            flash('Nursing home ID must use digits only.', category='error')
        elif len(nursing_home_id) < 6:
            flash('Nursing home ID must be at least 6 digits.', category='error')
        elif not agreeCheck:
            flash('Must agree to Terms and Conditions.', category='error')
        else:
            # Add new NursingHome
            new_nursing_home = NursingHome(id=nursing_home_id, name=nursing_home_name)
            db.session.add(new_nursing_home)
            db.session.commit()
            
            new_admin_account = User(email=email, password=password1, nursing_home_id=nursing_home_id, admin=True)
            db.session.add(new_admin_account)
            db.session.commit()
            
            # Add new Admin account associated with new Nursing
            # new_nursing_home = NursingHome(id=nursing_home_id, name=nursing_home_name, email=email, password=generate_password_hash(password1))
            # new_nursing_home = NursingHome(id=nursing_home_id, name=nursing_home_name, email=email, password=password1)
            
            # Add associated Guest for new NursingHome
            # new_guest_account = Guest(nursing_home_id=nursing_home_id)
            # db.session.add(new_guest_account)
            # db.session.commit()
            
            # login_user(new_user, remember=True)
            # flash('Account created!', category='success')
            # return redirect(url_for('views.home'))
            return render_template("sign_up_ver2.html", success='OK')

    return render_template("sign_up_ver2.html", user=current_user, success='')
