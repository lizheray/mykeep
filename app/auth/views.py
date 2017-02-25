from flask import render_template, session, redirect, url_for

from . import auth
from .forms import TestForm

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = TestForm()
    if form.validate_on_submit():
	session['name'] = form.email.data
	form.email.data = ''
	return redirect(url_for('.login'))
    return render_template('auth/login.html', form=form, name=session.get('name'))
