
import hashlib
from flask import Flask, render_template, request, redirect, url_for, abort, session
from Ejercicio03 import app
from Ejercicio03.forms import TaskForm, SelectTaskForm, TaskListForm, LoginForm
from Ejercicio03.models import Task
from Ejercicio03.utils import string_state

import Ejercicio03.database as database

@app.route('/')
def root():
    return render_template("inicio.html", message = "Crea, modifica y elimina las tareas de tu agenda.")


@app.route('/task/add', methods=['GET', 'POST'])
def add_task():

    form = TaskForm(False)
    form.estado.render_kw = {"disabled": True}
    form.estado.data = 0 #ESTADO DE PENDIENTE

    if form.validate_on_submit():
        
        task = Task(-1, form.fecha.data, form.descripcion.data, form.prioridad.data, form.estado.data)
        database.insert_task(task)

        return render_template("inicio.html", message = "Tarea creada correctamente.")

    else:
        return render_template("task_form.html", form = form, form_url = 'add_task', operation = "añadir")


@app.route('/task/update', methods=['GET', 'POST'])
def select_update_task():

    task_list = database.get_all_task()

    form = SelectTaskForm(task_list)

    if form.validate_on_submit():
        return redirect(url_for('update_task', task_id = form.id.data))

    else:
        return render_template("select_task.html", operation = "actualizar", 
                                                   task_list = task_list, 
                                                   form = form, 
                                                   form_url = 'select_update_task',
                                                   method = "POST")


@app.route('/task/update/<int:task_id>', methods=['GET', 'POST'])
def update_task(task_id):

    form = TaskForm(True)

    if not form.is_submitted():
        bind_data_task_form(form, database.get_task_by_id(task_id))

    if form.validate_on_submit():
        task = Task(task_id, form.fecha.data, form.descripcion.data, form.prioridad.data, form.estado.data)
        database.update_task(task)

        return render_template("inicio.html", message = "Tarea modifica correctamente.")

    else:
        return render_template("task_form.html", form = form, form_url = 'update_task', task_id = task_id, operation = "actualizar")


@app.route('/task/delete', methods=['GET', 'POST'])
def select_delete_task():

    task_list = database.get_all_task()

    form = SelectTaskForm(task_list, request.args)

    if len(request.args) > 0:
        if form.validate():
            database.delete_task(form.id.data)
            return render_template("inicio.html", message = "Tarea borrada correctamente.")

    return render_template("select_task.html", operation = "borrar", 
                                                task_list = task_list, 
                                                form = form, 
                                                form_url = 'select_delete_task',
                                                method = "GET")


def bind_data_task_form(form, task):
    """Inyecta los datos de la tarea en los campos del formulario
    
    Arguments:
        form {TaskForm} -- Formulario para inyectar los datos
        task {Task} -- Datos de la tarea
    """
    if(task == None): abort(404)

    form.fecha.data = task.fecha
    form.descripcion.data = task.descripcion
    form.prioridad.data = task.prioridad
    form.estado.data = task.estado


@app.route('/task/list', methods=['GET', 'POST'])
def task_list():

    filter = request.args.get('filter')

    filters = {
        'pending': lambda: database.get_state_task(0),
        'completed': lambda: database.get_state_task(2)
    }

    state = {
        'pending': 'pendientes',
        'completed': 'completadas'
    }

    if filter == None or filter == "form":
        task_list = database.get_all_task()
    else:
        if filter in filters:
            task_list = filters[filter]()
        else:
            abort(404)

    form = TaskListForm()

    if form.validate_on_submit():
        task_list = database.get_priority_state_task(form.prioridad.data, form.estado.data)
        filter = "form"

    estado = ""
    if filter in state:
        estado = state[filter]
    else:
        if form.estado.data != None:
            estado = string_state(form.estado.data, plural=True).lower()

    return render_template("task_list.html", form = form, task_list = task_list, filter = filter, operation = "listar", estado = estado)


@app.route('/login', methods=['GET', 'POST'])
def login():
    
    USERNAME_ADMIN = "admin"
    PASSWORD_ADMIN = "admin"

    USERNAME_USER = "user"
    PASSWORD_USER = "user"

    form = LoginForm()

    valid_login = True

    if request.method == 'POST' and form.validate_on_submit():

        admin_login = (form.username.data == USERNAME_ADMIN and form.password.data == PASSWORD_ADMIN)
        user_login = (form.username.data == USERNAME_USER and form.password.data == PASSWORD_USER)

        if admin_login or user_login:
            if admin_login:
                session["permission"] = "admin"
            else:
                session["permission"] = "user"

            session["username"] = form.username.data
            session["password"] = form.password.data
            return redirect(url_for('root'))

    return render_template("login_form.html", form = form, valid_login = valid_login)


@app.route('/logout', methods=['GET'])
def logout():
    session.pop("username")
    session.pop("password")

    return redirect(url_for('login'))


@app.before_request
def middleware():

    if("username" not in session and not request.endpoint == "login"):
        return redirect(url_for('login'))
    else:
        if session["permission"] == "user":
            if not user_point_permission(request.endpoint):
                return render_template("inicio.html", message = "Acceso restringido a usuarios administradores")


def user_point_permission(endpoint):

    allowed_endpoints = ["login", "logout", "root", "task_list"]

    return endpoint in allowed_endpoints;


@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html", error="Página no encontrada...")