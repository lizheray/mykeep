from flask import render_template, url_for, redirect, request, abort
from flask_login import current_user, login_required

from . import main
from ..models import User, Note, db
from .forms import NoteForm

@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Note.query.filter_by(isPublic=True).order_by(Note.timestamp.desc()).paginate(page, per_page=12, error_out=False)
    notes = pagination.items
    return render_template('index.html', notes=notes, pagination=pagination)

@main.route('/search')
def search():


    return render_template('search.html')

@main.route('/write', methods=['GET', 'POST'])
@login_required
def write():
    form = NoteForm()
    if form.validate_on_submit():
	note = Note(title=form.title.data, body=form.body.data, isPublic=form.isPublic.data, author=current_user._get_current_object())
	db.session.add(note)
	return redirect(url_for('.user', username=current_user.username))
    return render_template('write.html', form=form)

@main.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    if not user: abort(404)
    if current_user != user: abort(403)
    page = request.args.get('page', 1, type=int)
    pagination = user.notes.order_by(Note.timestamp.desc()).paginate(page, per_page=12, error_out=False)
    notes = pagination.items
    return render_template('user.html', notes=notes, pagination=pagination)

@main.route('/note/<int:id>')
def note(id):
    note = Note.query.get_or_404(id)
    if not note.isPublic and current_user != note.author: abort(403)
    return render_template('note.html', note=note)

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    note = Note.query.get_or_404(id)
    if current_user != note.author: abort(403)
    form = NoteForm()
    if form.validate_on_submit():
	note.title = form.title.data
	note.body = form.body.data
	note.isPublic = form.isPublic.data
	db.session.add(note)
	return redirect(url_for('.note', id=id))
    form.title.data = note.title
    form.body.data = note.body
    form.isPublic.data = note.isPublic
    return render_template('write.html', form=form)

@main.route('/delete/<int:id>')
@login_required
def delete(id):
    note = Note.query.get_or_404(id)
    if current_user != note.author: abort(403)
    db.session.delete(note)
    return redirect(request.referrer)

