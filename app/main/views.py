from flask import render_template
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

from . import main

@main.route('/')
def index():
    return render_template('index.html')

class TestForm(Form):
    email = StringField(validators=[Required()])
    submit = SubmitField('Submit')

@main.route('/login', methods=['GET', 'POST'])
def login():
    name = None
    form = TestForm()
    if form.validate_on_submit():
	name = form.email.data
	form.email.data = ''
    return render_template('login.html', form=form, name=name)
