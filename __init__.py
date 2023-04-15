from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import mysql.connector

db = SQLAlchemy()
db_name = 'flask_notes.db'
username = 'root'
password = 'mysql'
server = '127.0.0.1'
database = '/flask_notes'


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'nhaert'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://' + username + ':' + password + '@' + server + database
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


# def create_database(app):
#     mydb = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         passwd="mysql",
#         database="flask_notes"
#     )
#
#     my_cursor = mydb.cursor()
#
#     # my_cursor.execute("CREATE DATABASE our_users")
#     db.create_all(app=app)
#     my_cursor.execute("SHOW DATABASES")
#     for db in my_cursor:
#         print(db)
