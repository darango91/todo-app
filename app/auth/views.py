from . import auth

from app.forms import AuthForm
from app.firestore_service import get_user, user_put

from app.auth.models import UserData, UserModel

from flask import flash, render_template, redirect, request, url_for
from flask_login import login_user, login_required, logout_user

from werkzeug.security import check_password_hash, generate_password_hash


@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = AuthForm()

    context = {
        'login_form': login_form,
    }

    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data

        user_dict = get_user(username).to_dict()

        if user_dict is not None:
            if check_password_hash(user_dict['password'], password):
                user_data = UserData(username, password)
                user = UserModel(user_data)
                login_user(user, remember=True)

                flash('Bienvenido de nuevo!')

                next_page = request.args.get('next')
                return redirect(next_page or url_for('hello'))
            else:
                flash('La informacion no coincide', category='warning')
        else:
            flash('El usuario no existe', category='error')

    return render_template('login.html', **context)


@auth.route('logout')
@login_required
def logout():
    logout_user()
    flash('Regresa pronto')

    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_form = AuthForm()

    context = {
        'signup_form': signup_form,
    }

    if signup_form.validate_on_submit():
        username = signup_form.username.data
        password = signup_form.password.data

        user_dict = get_user(username).to_dict()

        if user_dict is None:
            password_hash = generate_password_hash(password)
            user_data = UserData(username, password_hash)
            user_put(user_data)

            user = UserModel(user_data)
            login_user(user)
            flash('Bienvenido!')

            return redirect(url_for('hello'))
        else:
            flash('El usuario ya existe', category='error')

    return render_template('signup.html', **context)
