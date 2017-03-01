from flask_wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import Required, Length

class NoteForm(Form):
    title = StringField(validators=[Required(), Length(1, 64)])
    body = TextAreaField(validators=[Required()])
    isPublic = BooleanField()
    submit = SubmitField('Submit')
