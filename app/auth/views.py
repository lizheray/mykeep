from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required

from . import auth
from ..models import User
from .forms import LoginForm

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
    
