from flask import Flask, request, redirect, render_template, session, flash
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
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


@app.route("/login")
def login():
    """Login Page."""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if(user is not None and user.verify_password(form.password.data)):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get("next") or "/")
    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    """Logout Page."""
    logout_user()
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect("/login")
    return render_template("register.html", form=form)
