from datetime import datetime

from flask import Blueprint, render_template, request, flash, json, jsonify, url_for, redirect
from flask_login import login_required, current_user
import json

from sqlalchemy.sql import func

from app import db
from models import Note, User

views = Blueprint('views', __name__)


# View notes and add a new note
@views.route('/', methods=['GET', 'POST'])
@login_required
def index():  # put application's code here
    if request.method == 'POST':
        note = request.form.get('note')  # Gets the note from the HTML
        title = request.form.get('title')
        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(content=note, user_id=current_user.id, title=title, date_created=datetime.utcnow(),
                            last_edited=datetime.utcnow())  # ,
            db.session.add(new_note)  # adding the note to the database
            db.session.commit()
            flash('Note added!', category='success')
    return render_template("index.html", user=current_user)  # , notes=notes)


# Delete a note
@login_required
@views.route('/delete-note/<int:id>', methods=['GET', 'POST'])
def delete_note(id):
    note = Note.query.get_or_404(id)
    try:
        db.session.delete(note)
        db.session.commit()
        return render_template("index.html", user=current_user)
    except:
        return '<h1>Something is broken.</h1>' \
                   '<p>There was a problem editing that task.</p>'


# Edit a note
@login_required
@views.route('/edit-note/<int:id>', methods=['GET', 'POST'])
def edit_note(id):
    # notes = current_user.notes
    # updated_note = notes.get(id)
    updated_note = Note.query.get_or_404(id)
    if request.method == 'GET':
        return render_template("edit-note.html", user=current_user, note=updated_note)
    elif request.method == 'POST':
        note = request.form.get('note')  # Gets the note from the HTML
        title = request.form.get('title')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            updated_note.content = note
            updated_note.title = title
            updated_note.last_edited = datetime.utcnow()
            try:
                db.session.commit()
                flash('Note added!', category='success')
                return render_template("index.html", user=current_user)
            except:
                return '<h1>Something is broken.</h1>' \
                   '<p>There was a problem editing that task.</p>'


# View a note
@login_required
@views.route('/view-note/<int:id>', methods=['GET'])
def view_note(id):
    note = Note.query.get_or_404(id)
    return render_template("view-note.html", user=current_user, note=note)


# Invalid URL
@views.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", user=current_user), 404


# Internal Server error
@views.errorhandler(500)
def server_error(e):
    return render_template("500.html", user=current_user), 500


# User account information
@login_required
@views.route('/user-account/<int:id>')
def user_account(id):
    user = User.query.query.get_or_404(id)
    return render_template("user-info.html", user=current_user)

