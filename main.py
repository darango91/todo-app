import unittest

from app import create_app

from flask import flash, make_response, request, redirect,\
    render_template, session, url_for
from flask_login import login_required, current_user

from app.firestore_service import get_todos, put_todo, delete_todo, update_todo
from app.forms import DeleteTodoForm, ToDoForm, UpdateTodoForm

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
    todos = get_todos(username)
    todo_form = ToDoForm()
    delete_form = DeleteTodoForm()
    update_form = UpdateTodoForm()

    context = {
        'user_ip': user_ip,
        'todos': todos,
        'username': username,
        'todo_form': todo_form,
        'delete_form': delete_form,
        'update_form': update_form,
    }

    if todo_form.validate_on_submit():
        put_todo(username, todo_form.description.data)
        flash('Tarea creada exitosamente')
        redirect(url_for('index'))

    return render_template('hello.html', **context)


@app.route('/todos/delete/<todo_id>', methods=['POST'])
@login_required
def delete(todo_id):
    user_id = current_user.id
    delete_todo(user_id, todo_id)

    return redirect(url_for('hello'))


@app.route('/todos/update/<todo_id>/<int:done>', methods=['POST'])
@login_required
def update(todo_id, done):
    user_id = current_user.id
    update_todo(user_id=user_id, todo_id=todo_id, done=done)

    return redirect(url_for('hello'))
