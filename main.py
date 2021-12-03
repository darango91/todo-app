import unittest

from app import create_app

from flask import flash, make_response, request, redirect,\
    render_template, session, url_for
from flask_login import login_required, current_user

from app.firestore_service import get_todos, put_todo
from app.forms import ToDoForm

app = create_app()


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)


@app.errorhandler(500)
def server_error(error):
    return render_template('500.html', error=error)


@app.route('/')
def index():
    user_ip = request.remote_addr
    response = make_response(redirect('/hello'))
    session['user_ip'] = user_ip
    return response


@app.route('/hello', methods=['GET', 'POST'])
@login_required
def hello():
    user_ip = session.get('user_ip')
    username = current_user.id
    todos = [todo.to_dict()['description'] for todo in get_todos(username)]
    todo_form = ToDoForm()

    context = {
        'user_ip': user_ip,
        'todos': todos,
        'username': username,
        'todo_form': todo_form
    }

    if todo_form.validate_on_submit():
        put_todo(username, todo_form.description.data)
        flash('Tarea creada exitosamente')
        redirect(url_for('hello'))

    return render_template('hello.html', **context)
