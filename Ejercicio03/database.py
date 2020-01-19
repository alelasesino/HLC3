
import mysql.connector
from contextlib import closing
from Ejercicio03.models import Task, User
import Ejercicio03.encryption as encryption


db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="paises"
)


def get_all_task():
    """Obtiene todas las tareas de la agenda
    
    Returns:
        array tuples -- (ID, FECHA, DESCRIPCION, PRIORIDAD, ESTADO) de la tarea
    """
    with closing(db.cursor()) as c:

        sql_query = "SELECT id, fecha, descripcion, prioridad, estado FROM agenda"
        c.execute(sql_query)

        tasks = []

        for (id, fecha, descripcion, prioridad, estado) in c:
            tasks.append(Task(id, fecha, descripcion, prioridad, estado))

    return tasks


def get_state_task(state: int):

    with closing(db.cursor()) as c:
            
        sql_query = "SELECT id, fecha, descripcion, prioridad, estado FROM agenda WHERE estado = %s"
        c.execute(sql_query, [state])

        tasks = []

        for (id, fecha, descripcion, prioridad, estado) in c:
            tasks.append(Task(id, fecha, descripcion, prioridad, estado))

    return tasks


def get_priority_task(priority: int):

    with closing(db.cursor()) as c:
            
        sql_query = "SELECT id, fecha, descripcion, prioridad, estado FROM agenda WHERE prioridad = %s"
        c.execute(sql_query, [priority])

        tasks = []

        for (id, fecha, descripcion, prioridad, estado) in c:
            tasks.append(Task(id, fecha, descripcion, prioridad, estado))

    return tasks


def get_priority_state_task(priority: int, state: int):
    """Obtiene las tareas con el estado y la prioridad deseada
    
    Keyword Arguments:
        priority {int} -- Prioridad de la tarea: 0, 1, 2, 3, 4, 5 (default: {""})
        state {int} -- Estado de la tarea: 0: Pendiente, 1:En proceso, 2:Completada (default: {""})
    
    Returns:
        ARRAY TUPLES -- (ID, FECHA, DESCRIPCION, PRIORIDAD, ESTADO) de la tarea
    """

    with closing(db.cursor()) as c:
        
        sql_query = "SELECT id, fecha, descripcion, prioridad, estado FROM agenda WHERE prioridad = %s AND estado = %s"
        c.execute(sql_query, (priority, state))

        tasks = []

        for (id, fecha, descripcion, prioridad, estado) in c:
            tasks.append(Task(id, fecha, descripcion, prioridad, estado))

    return tasks


def get_task_by_id(task_id: int):
    """Obtiene los datos de una tarea por su id
    
    Arguments:
        task_id {int} -- Id de la tarea
    
    Returns:
        Task -- Datos de la tarea seleccionada
    """
    with closing(db.cursor()) as c:

        sql_query = "SELECT id, fecha, descripcion, prioridad, estado FROM agenda WHERE id = %s"
        c.execute(sql_query, [task_id])
        
        result = c.fetchone()

        if result != None:
            (id, fecha, descripcion, prioridad, estado) = result

            return Task(id, fecha, descripcion, prioridad, estado)


def insert_task(task: Task):
    """Inserta una nueva tarea en la base de datos
    
    Arguments:
        task {Task} -- Tarea para insertar
    """
    with closing(db.cursor()) as c:

        sql_query = "INSERT INTO agenda(fecha, descripcion, prioridad, estado) VALUES(%s, %s, %s, %s)"
        c.execute(sql_query, (task.fecha, task.descripcion, task.prioridad, task.estado))
        db.commit()


def delete_task(task_id: int):
    """Elimina la tarea deseada en la base de datos
    
    Arguments:
        task_id {int} -- Id de la tarea para borrar
    """
    with closing(db.cursor()) as c:
        
        sql_query = "DELETE FROM agenda WHERE id = %s"
        c.execute(sql_query, [task_id])
        db.commit()


def update_task(task: Task):
    """Actualiza la tarea deseada en la base de datos
    
    Arguments:
        task {Task} -- Tarea para actualizar
    """
    with closing(db.cursor()) as c:
        
        sql_query = "UPDATE agenda SET fecha = %s, descripcion = %s, prioridad = %s, estado = %s WHERE id = %s"
        c.execute(sql_query, (task.fecha, task.descripcion, task.prioridad, task.estado, task.id))
        db.commit()


def insert_user(user: User):
    """Inserta un nuevo usuario en la base de datos
    
    Arguments:
        user {User} -- Usuario para insertar
    """
    with closing(db.cursor()) as c:

        sql_query = "INSERT INTO usuario VALUES(%s, %s, %s, %s)"
        c.execute(sql_query, (user.username, user.password, user.nickname, user.permission))
        db.commit()


def get_user_by_username(username: str):
    """Obtiene los datos de un usuario
    
    Arguments:
        username {str} -- Nombre de usuario
    
    Returns:
        User -- Datos del usuario
    """
    with closing(db.cursor()) as c:

        sql_query = "SELECT username, password, nickname, permission FROM usuario WHERE username = %s"
        c.execute(sql_query, [username])
        
        result = c.fetchone()

        if result != None:
            (username, password, nickname, permission) = result
            password = encryption.decrypt(password)

            return User(username, password, nickname, permission)

