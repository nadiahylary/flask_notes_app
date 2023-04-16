from datetime import datetime

from flask import Blueprint, render_template, request, flash, json, jsonify
from flask_login import login_required, current_user
import json

from sqlalchemy.sql import func

from app import db
from models import Note

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def index():  # put application's code here
    if request.method == 'POST':
        note = request.form.get('note')  # Gets the note from the HTML
        title = request.form.get('title')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(content=note, user_id=current_user.id, title=title, date_created=datetime.utcnow(), last_edited=datetime.utcnow())  #  ,
            db.session.add(new_note)  # adding the note to the database
            db.session.commit()
            flash('Note added!', category='success')
    notes = Note.query.order_by(Note.date_created).all()
    return render_template("index.html", user=current_user)  # , notes=notes)


@views.route('/delete-note/<int:id>', methods=['POST'])
def delete_note(id):
    pass


@views.route('/edit-note/<int:id>', methods=['POST'])
def edit_note(id):
    pass