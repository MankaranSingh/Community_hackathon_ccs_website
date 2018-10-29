from flask import render_template, session, redirect, url_for, flash, redirect, current_app
from . import main
from .forms import Login, SignUp, SignUp_society, Admin_form, Account_form,Post_form
from .. import db, login_manager
from ..models.users import User, Role, Society, Post
from werkzeug import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug import generate_password_hash
from flask_mail import Message
import secrets


@main.route('/Home',methods = ['GET', 'POST'])
def home():
    return render_template('HomePage.html',post = Post.query.all())

@main.route('/Post', methods = ['GET', 'POST'])
@login_required
def post():
    form = Post_form()
    if form.validate_on_submit():
        if current_user.society_name!=form.society_name.data:
            flash('Account Not Linked With Society')
        else:
            post = Post(society_name = form.society_name.data, post_title= form.post_title.data, post_body = form.post_body.data, post_author = current_user.username)
            db.session.add(post)
            db.session.commit()
            flash('Post Successfully Created')
    return render_template('Post.html', form = form)
            


@main.route('/Account', methods = ['GET', 'POST'])
@login_required
def account():
    form = Account_form()
    form.username.data = str(current_user.username)
    form.email.data = str(current_user.email)
    form.year.data = current_user.year
    form.phone_number.data = current_user.phone_number
    form.roll_number.data = current_user.roll_number
    if form.validate_on_submit():
        current_user.username=form.username.data
        current_user.email = form.email.data
        current_user.year = form.year.data
        current_user.phone_number = form.phone_number.data
        current_user.roll_number = form.roll_number.data
        db.session.commit()
        flash('Account Info Updated.')
    return render_template('Account.html', form = form)

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
@login_required
def SignUp_Head():
    form = SignUp_society()
    if form.validate_on_submit():
        society = Society.query.filter_by(society_name = form.society_name.data).first()
        if society is not None:
            '''
            head = User.query.filter_by(society = form.society_name.data, society_head = True)
            if head is None:
                flag = False
            else:
                flag = True
                '''
            user = User.query.filter_by(email = current_user.email)
            if user:
                if form.Secret_key.data == society.secret_key:
                    current_user.society_name = form.society_name.data
                    current_user.society_head = True
                    db.session.commit()
                    flash('Successfully linked account with society.')
                    
                    return redirect(url_for('main.home'))
                else:
                    flash('Invalid Secret Key')
                
            else:
                flash('Invalid Cradentials or Secret Key')
    return render_template('Register_Head.html', form = form)
                
@main.route('/Login', methods=['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user,form.remember.data)
            flash('Logged In')
            return redirect(url_for('main.home'))
        else:
            flash('Login Failed, Incorrect Username or Password Entered')
    return render_template('Login.html', form = form)

@main.route('/SignUp', methods=['GET', 'POST'])
def sign_up():
    form = SignUp()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username = form.username.data, email = form.email.data, password= hashed_password, phone_number = form.phone_number.data, year = form.year.data, roll_number = form.roll_number.data)
        #Role.insert_roles()
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


    

    
            
            
        
            
