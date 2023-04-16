from flask_login import UserMixin
from sqlalchemy.sql import func
from . import db
import sqlalchemy.orm


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    is_loggedin = db.Column(db.Boolean, default=False, nullable=False)
    notes = db.relationship('Note', backref="user")
    # , backref='user', lazy=True cascade="all, delete, delete-orphan",
    #     single_parent=True,
    #     order_by="desc(Note.date_created)"



class Note(db.Model):
    __tablename__ = "notes"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.String(10000), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now)
    last_edited = db.Column(db.DateTime(timezone=True))
    user_id = db.Column(db.Integer, db.Foreignkey('user.id'))
