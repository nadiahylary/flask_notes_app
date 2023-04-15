from app import app
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

app.config['SECRET_KEY'] = 'nhaert'
db = SQLAlchemy()

# change string to the name of your database; add path if necessary
db_name = 'flask_notes.db'
username = 'root'
password = 'mysql'
server = '127.0.0.1'
database = '/flask_notes'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + username + ':' + password + '@' + server + database


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(25), nullable=False)
    password = db.Column(db.String(20), nullable=False)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Foreignkey)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.String(2000), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    last_edited = db.Column(db.DateTime)
