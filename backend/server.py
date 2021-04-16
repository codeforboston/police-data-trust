from flask import Flask, request, redirect, render_template, session, flash
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from flask_login import LoginManager, login_user, logout_user
from flask_user import current_user, login_required, roles_required, UserManager
from api import app
from user import User
from backend.incidents import db
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, FileField, BooleanField, ValidationError
from wtforms.validators import Required, Length, Email, Regexp, EqualTo

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.init_app(app)

 # Flask-Mail SMTP server settings
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TLS = False
MAIL_USERNAME = 'email@example.com'
MAIL_PASSWORD = 'password'
MAIL_DEFAULT_SENDER = '"MyApp" <noreply@example.com>'

# Flask-User settings
USER_APP_NAME = "Police Data Trust"      # Shown in and email templates and page footers
USER_ENABLE_EMAIL = True                 # Enable email authentication
USER_ENABLE_USERNAME = False             # Disable username authentication
USER_EMAIL_SENDER_NAME = USER_APP_NAME
USER_EMAIL_SENDER_EMAIL = "noreply@example.com" 


###########
## FORMS ##
###########

class RegistrationForm(FlaskForm):
    email = StringField('Email:', validators=[Required(),Length(1,64),Email()])
    username = StringField('Username:',validators=[Required(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'Usernames must have only letters, numbers, dots or underscores')])
    password = PasswordField('Password:',validators=[Required(),EqualTo('password2',message="Passwords must match")])
    password2 = PasswordField("Confirm Password:",validators=[Required()])
    submit = SubmitField('Register User')
 
    #Additional checking methods for the form
    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
 
    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already taken')
 
# Provided
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1,64), Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

###########
## LOGIN ##
###########

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login Page."""
    # form = LoginForm()
    form = request.form
    if form['password'] != '' and form['email'] != '':
        user = User.query.filter_by(email=form['email']).first()
        if(user is not None and user.verify_password(form['password'])):
            login_user(user, form['remember_me'])
            # return redirect(request.args.get("next") or "/")
            return {"status":"ok", "message": "Successfully logged in.", "user": { "email": form['email']}}
        else
            return {"status":"ok", "message": "Error. Username or Password invalid."}
    missing_fields = ""
    for field in form:
        if field == '':
            missing_fields= missing_fields + ", " + field
    return {"status":"ok", "message": "Failed to log in. Please include the following fields: " + missing_fields}

@app.route("/logout")
@login_required
def logout():
    """Logout Page."""
    logout_user()
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    # form = RegistrationForm()
    form = request.form
    if form['username'] != '' and form['password'] != '' and form['email'] != '':
        user = User(email=form['email'], username=form['username'], password=form['password'])
        db.session.add(user)
        db.session.commit()
        # return redirect("/login")
        return {"status":"ok", "message": "Successfully registered.", "user": { "email": form['email'], "username": form['username']}}
    missing_fields = ""
    for field in form:
        if field == '':
            missing_fields= missing_fields + ", " + field

    return {"status":"ok", "message": "Failed to register. Please include the following fields: " + missing_fields}
