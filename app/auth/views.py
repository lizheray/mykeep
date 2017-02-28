import re
from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required

from . import auth
from ..models import User, db
from .forms import LoginForm, RegistrationForm

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    notValid = False
    if form.validate_on_submit():
	user = User.query.filter_by(email=form.email.data).first()
	if user and user.verify_password(form.password.data):
	    login_user(user, form.remember_me.data)
	    return redirect(request.args.get('next') or url_for('main.index'))
        notValid = True
    return render_template('auth/login.html', form=form, notValid=notValid)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
    
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    existEmail = False
    existUsername = False
    invalidUsername = False
    dismatchpsd = False
    if form.validate_on_submit():
	if User.query.filter_by(email=form.email.data).first():
	    existEmail = True
	elif User.query.filter_by(username=form.username.data).first():
	    existUsername = True
	elif not re.match('^[A-Za-z][A-Za-z0-9_.]*$', form.username.data):
	    invalidUsername = True
	elif form.password2.data != form.password.data:
	    dismatchpsd = True
	else:
	    user = User(email=form.email.data, username=form.username.data, password=form.password.data)
	    db.session.add(user)
	    return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form, existEmail=existEmail, existUsername=existUsername, dismatchpsd=dismatchpsd, invalidUsername=invalidUsername)
