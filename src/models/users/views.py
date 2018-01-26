from flask import Blueprint, request, url_for, redirect, session, render_template

from src.common.database import Database
from src.models.users.decorators import requires_login
from src.models.users.user import User

from src.models.users.errors import UserNotExistsError, IncorrectPasswordError, UserError

user_blueprint = Blueprint('users', __name__)

@user_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            if User.login_is_valid(email, password):
                session['email'] = email
                return redirect(url_for(".user_alerts"))
        except UserError as e:
            return render_template("users/login_failed.html", message=e.message)

    return render_template("users/login.html")


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            if User.register_user(email, password):
                session['email'] = email
                return redirect(url_for(".user_alerts"))
        except UserError as e:
            return render_template("users/login_failed.html", message=e.message)  # TODO: change this

    return render_template("users/register.html")


@user_blueprint.route('/alerts')
@requires_login
def user_alerts():
    user = User.get_from_email(session['email'])
    alerts = user.get_alerts()
    return render_template("users/alerts.html", alerts=alerts)


@user_blueprint.route('/logout')
def logout_user():
    session['email'] = None
    return redirect(url_for('home'))


@user_blueprint.route('/check_alerts/<string:user_id>')
def check_user_alerts(user_id):
    pass