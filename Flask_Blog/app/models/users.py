from .. import db, login_manager, mail
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, render_template
from flask_mail import Message


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Permission:

    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_POST = 0x03
    MODERATE_COMMENTS = 0x08
    ADMINISTRATOR = 0x80 

class Role(db.Model, UserMixin ):

    __tablename__ = 'roles'

    role_name =  db.Column(db.String(50), unique = True)
    id = db.Column(db.Integer, primary_key = True)
    users = db.relationship('User' , backref = 'role', lazy = 'dynamic' )
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)

    @staticmethod
    def insert_roles():

        roles = {'User': (Permission.FOLLOW | Permission.COMMENT | Permission.WRITE_POST, True), 
                 'Moderator': (Permission.FOLLOW | Permission.COMMENT | Permission.WRITE_POST | Permission.MODERATE_COMMENTS, False),
                 'Administrator':( Permission.FOLLOW | Permission.COMMENT | Permission.WRITE_POST | Permission.MODERATE_COMMENTS | Permission.ADMINISTRATOR, False)}
'''
        for r in roles:
            if Role.query.filter_by(role_name = str(r)).first() is None:
                role = Role(role_name = str(r))
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()
'''               
                

class User(db.Model, UserMixin):

    __tablename__ = 'users'
    
    username = db.Column(db.String(50), unique = True, nullable = False)
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    role_id = db.Column(db.Integer , db.ForeignKey('roles.id'))
    email = db.Column(db.String(120), unique= True, nullable = False)
    password = db.Column(db.String(120), nullable = False)
    confirmed = db.Column(db.Boolean, default = False)

    def generate_confirmation_token(self, expiration = 3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm':self.id})

    def confirm(self,token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm')!= self.id:
            return False
        self.confirm = True
        db.session.add(self)
        return True

    def send_mail(to, subject, template, **kwargs):
        msg = Message(subject, sender = 'mankaran32@gmail.com',
                      recipients = [str(to)])
        msg.body = render_template(str(template) + '.txt', **kwargs)
        mail.send(msg)

    def can(self, permissions):
        if self.role.permissions == permissions:
            return True
        return False
    def is_admin(self):
        if self.role.permissions == Permission.ADMINISTRATOR:
            return True
        return False


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


    

        
    
