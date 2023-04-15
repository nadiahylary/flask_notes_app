import re

from flask import Blueprint, render_template, request, flash

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
        if not email_validation(request.form.get('email')):
            flash("Please enter a valid email address", category='error')
        else:
            # check if email already exists in db
            # if it doesn't exist yet:
            if not password_val(request.form.get('password')) \
                    or password_val(request.form.get('conf-password')):
                flash("Password should be at least 8 letters long with capital/small"
                      " letters and one special character.", category='error')
            elif request.form.get('password') != request.form.get('conf-password'):
                flash("The passwords don't match", category='error')
            elif request.form.get('name') == "":
                flash("Please enter your name", category='error')
            else:
                pass
                # add new user to db
    else:
        return render_template('sign-up.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if not email_validation(request.form.get('email')):
            flash("Please enter a valid email address", category='error')
        else:
            pass
            # and check if submitted email exist in db
            # if email exists:
            if not password_val(request.form.get('password')):
                flash("The password is incorrect.", category='error')
            else:
                pass
                # and check if submitted pass == user.pass
                # if pass correct allow login
    else:
        return render_template('login.html')


@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    return "Logout"


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

