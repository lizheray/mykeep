from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

class TestForm(Form):
    email = StringField(validators=[Required()])
    submit = SubmitField('Submit')
