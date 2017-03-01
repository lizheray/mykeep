from flask import render_template, url_for, redirect
from flask_login import current_user, login_required

from . import main
from ..models import User, Note, db
from .forms import NoteForm

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/write', methods=['GET', 'POST'])
@login_required
def write():
    form = NoteForm()
    if form.validate_on_submit():
	note = Note(title=form.title.data, body=form.body.data, isPublic=form.isPublic.data, author=current_user._get_current_object())
	db.session.add(note)
	return redirect(url_for('.index'))
    notes = Note.query.order_by(Note.timestamp.desc()).all()
    return render_template('write.html', form=form, notes=notes)

@main.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    notes = user.notes.order_by(Note.timestamp.desc()).all()
    return render_template('user.html', user=user, notes=notes)
