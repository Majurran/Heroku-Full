from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, NursingHome
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


"""
LOGIN PAGE RANDOM NOTES:
    Add the radiobox option whether to sign in as admin or guest? Instead of creating a separate guest account each time 
    for each nursing home from the signup page. Though it does create some security risk if the staff member saves the 
    account email and password to the web browser, but can assume that they don't do that? Oh well it's just a prototype anyway.
"""
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Might change this
        homeID = request.form.get('homeId')
        print(homeID)

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                # flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

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
        
        # Creates the one admin profile for each nursing home for now
        nursing_home_name = request.form.get('nursing-home-name')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        # Might change this 
        agreeCheck = request.form.get('agreeCheck')
        staffId = request.form.get('staffId')
        homeId = request.form.get('homeId')
        admin = True # Can remove if using the radiobox signin feature

        # Look up email and nursing home name to see if they exist in the database already
        user = User.query.filter_by(email=email).first()
        existing_nursing_home_name = NursingHome.query.filter_by(name=nursing_home_name).first()
        if user:
            flash('Email already exists.', category='error')
        elif existing_nursing_home_name:
            flash('Nursing Home Name already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 6:
            flash('Password must be at least 6 characters.', category='error')
        else:
            # Add new NursingHome
            new_nursing_home = NursingHome(activity_list=activity_list, wellbeing_list=wellbeing_list, name=nursing_home_name)
            db.session.add(new_nursing_home)
            db.session.commit()
            
            # Add new User
            new_user = User(admin=admin, email=email, password=generate_password_hash(password1, method='sha256'), nursing_home_id=new_nursing_home.id) 
            db.session.add(new_user)
            db.session.commit()
            
            # login_user(new_user, remember=True)
            # flash('Account created!', category='success')
            # return redirect(url_for('views.home'))
            return render_template("sign_up_ver2.html", success='OK')

    return render_template("sign_up_ver2.html", user=current_user, success='')
