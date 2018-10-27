from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField , PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Email
from .. import db
from ..models.users import User, Role, Society
from flask_login import current_user

class Admin_form(FlaskForm):

    Society_name = StringField('Society Name: ' , validators= [Length(3,50), DataRequired()])
    society_secret_key = StringField('Secret Key: ' , validators= [Length(1,120), DataRequired()])
    submit = SubmitField('Register')
    def validate_Society_name(self, society_name):
        society = Society.query.filter_by(society_name = society_name.data).first()
        if society:
            raise ValidationError('Username Already Taken')
    def validate_society_secret_key(self, society_secret_key):
        secret_key = Society.query.filter_by(secret_key = society_secret_key.data).first()
        if secret_key:
            raise ValidationError('Secret Key Already In Use')
        

class SignUp(FlaskForm):

    username = StringField('Username: ' , validators= [Length(3,50), DataRequired()])
    email = StringField('Email: ', validators= [Email()])
    password = PasswordField('Password: ' ,validators= [Length(3,50), DataRequired()])
    confirm_password = PasswordField('Confirm Password: ' ,validators= [Length(3,50), DataRequired(), EqualTo('password', message='Passwords must match')])
    Submit = SubmitField('Sign Up !')

    def validate_username(self, username):

        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('Username Already Taken')
    def validate_email(self, email):

        email = User.query.filter_by(email = email.data).first()
        if email:
            raise ValidationError('Email Already in Use')

class Login(FlaskForm):


    email = StringField('Email: ', validators = [Email()])
    password = PasswordField('Password: ' ,validators= [Length(3,50), DataRequired()])
    remember = BooleanField('Remember Me')
    Submit = SubmitField('Login')

class SignUp_society(FlaskForm):

    society_name = StringField('Society Name:', validators = [DataRequired(), Length(1,100)])
    email = StringField('Email: ', validators= [Email()])
    Secret_key = StringField('Secret Key:', validators = [DataRequired()])
    Submit = SubmitField('Register')
    
    
    def validate_email(self, email):

        email = User.query.filter_by(email = current_user.email).first()
        if not email:
            raise ValidationError('Invalid Cradentials')

    def validate_society_name(self, society_name):

        society = Society.query.filter_by(society_name = society_name.data).first()
        if not society:
            raise ValidationError('Society does not exists. Contact Administrator.')
        

            
       



    
    
    
    
