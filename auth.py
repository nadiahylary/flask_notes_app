import re

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, current_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from models import User

auth = Blueprint('auth', __name__)

# The regular expression below checks that a password:
#
# Has minimum 8 characters in length. Adjust it by modifying {8,}
# At least one uppercase letter. You can remove this condition by removing (?=.*?[A-Z])
# At least one lowercase letter.  You can remove this condition by removing (?=.*?[a-z])
# At least one digit. You can remove this condition by removing (?=.*?[0-9])
# At least one special character,  You can remove this condition by removing (?=.*?[#?!@$%^&*-])
password_pattern = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"

email_re = r"^\S+@\S+\.\S+$"
email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
email_pattern = r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_" \
                r"`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = str(request.form.get('password'))
        conf_password = str(request.form.get('conf_password'))

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Your Email already exists.', category='error')
        elif not email_validation(email):
            flash('Your Email must be greater than 3 characters.', category='error')
        elif len(name) < 2:
            flash('Your name must be greater than 1 character.', category='error')
        elif password != conf_password:
            print(password, conf_password)
            flash('Passwords don\'t match.', category='error')
        elif len(password) < 8:
            flash('The Password must be at least 8 characters.', category='error')
        else:
            new_user = User(username=name, email=email, password=generate_password_hash(password, method='sha256'), is_loggedin=True )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.index'))

    return render_template("sign-up.html", user=current_user)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                user.is_loggedin = True
                login_user(user, remember=True)
                return redirect(url_for('views.index'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/forgot-pass', methods=['GET', 'POST'])
def forgot_pass():
    return render_template('forgot-password.html')


@auth.route('/reset-pass', methods=['GET', 'POST'])
def reset_pass():
    return render_template('reset-password.html')


def email_validation(email):
    return re.match(email_regex, email)


def password_val(password):
    return re.match(password_pattern, password)

