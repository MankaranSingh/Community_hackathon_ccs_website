from flask import render_template, session, redirect, url_for, flash, redirect, current_app
from . import main
from .forms import Login, SignUp
from .. import db, login_manager
from ..models.users import User, Role
from werkzeug import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug import generate_password_hash
from flask_mail import Message


@main.route('/Home')

def home():
    return render_template('HomePage.html')

@main.route('/Login', methods=['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user,form.remember.data)
            flash('Logged In')
            redirect(url_for('main.home'))
        else:
            flash('Login Failed, Incorrect Username or Password Entered')
    return render_template('Login.html', form = form)

@main.route('/SignUp', methods=['GET', 'POST'])
def sign_up():
    form = SignUp()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username = form.username.data, email = form.email.data, password= hashed_password)
        Role.insert_roles()
        user.role = Role.query.filter_by(role_name = 'User').first()
        db.session.add(user)
        db.session.commit()
        flash('Your Acount has been successfuly registered, A confirmation E-mail been sent to your emai address. ')
        #token = user.generate_confirmation_token()
        #User.send_mail(user.email, 'Confirm Account' , 'confirmation_email'
        #             , user = user, token = token)
        return redirect(url_for('main.login'))
    return render_template('Register.html', form = form)

@main.route('/confirm/<token>')
@login_required
def confirm_id(token):
    if current_user.confirmed:
        return redirect(url_for('main.home'))
    if current_user.confirm(token):
        flash('You have confirmed your account.')
    else:
        flash('The confirmation link is invalid or has expired.')
        return redirect(url_for('main.home'))
                            
@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged Out')
    return redirect(url_for('main.home'))


    

    
            
            
        
            
