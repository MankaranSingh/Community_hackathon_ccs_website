from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField , PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Email
from .. import db
from ..models.users import User

EqualTo('confirm', message='Passwords must match')

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

    
    
    
