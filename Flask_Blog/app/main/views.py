from flask import render_template, session, redirect, url_for, flash, redirect, current_app
from . import main
from .forms import Login, SignUp, SignUp_society, Admin_form
from .. import db, login_manager
from ..models.users import User, Role, Society
from werkzeug import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug import generate_password_hash
from flask_mail import Message
import secrets


@main.route('/Home')

def home():
    return render_template('HomePage.html')

@main.route('/Admin', methods = ['GET', 'POST'])
@login_required
def Admin_Page():
    form = Admin_form()
    secret = secrets.token_hex(4)
    if current_user.email == 'mankaran32@gmail.com':
        if form.validate_on_submit():
            society = Society(society_name = form.Society_name.data, secret_key= form.society_secret_key.data)
            db.session.add(society)
            db.session.commit()
            flash('Society Registered')
    else:
        return redirect(url_for('main.home'))
    return render_template('Admin.html', form = form, secret = secret)
        
@main.route('/Sign_up_Society_head', methods = ['GET', 'POST'] )
def SignUp_Head():
    form = SignUp_society()
    if form.validate_on_submit():
        society = Society.query.filter_by(society = form.society_name.data).first()
        if society is not None:
            head = User.query.filter_by(soociety = form.society_name.data, society_head = True)
            if head is None:
                flag = False
            else:
                flag = True
            hashed_password = generate_password_hash(form.password.data)
            user = User(username = form.username.data, email = form.email.data, password= hashed_password, Society_name = form.society_name.data, society_head = flag)
            if form.secret_key.data == society_user.secret_key:
                db.session.add(user)
                db.session.commit()
                flash('Your  Society Account has been successfuly registered, A confirmation E-mail been sent to your emai address. ')
                #token = user.generate_confirmation_token()
                #User.send_mail(user.email, 'Confirm Account' , 'confirmation_email'
                #             , user = user, token = token)
                return redirect(url_for('main.login'))
    return render_template('Register_Head.html', form = form)
                
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
        #user.role = Role.query.filter_by(role_name = 'User').first()
        db.session.add(user)
        db.session.commit()
        flash('Your Account has been successfuly registered, A confirmation E-mail been sent to your emai address. ')
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


    

    
            
            
        
            
