
import mysql.connector
from contextlib import closing
from Ejercicio03.models import Task

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


def get_state_task(state):

    with closing(db.cursor()) as c:
            
        sql_query = "SELECT id, fecha, descripcion, prioridad, estado FROM agenda WHERE estado = %s"
        c.execute(sql_query, [state])

        tasks = []

        for (id, fecha, descripcion, prioridad, estado) in c:
            tasks.append(Task(id, fecha, descripcion, prioridad, estado))

    return tasks


def get_priority_task(priority):

    with closing(db.cursor()) as c:
            
        sql_query = "SELECT id, fecha, descripcion, prioridad, estado FROM agenda WHERE prioridad = %s"
        c.execute(sql_query, [priority])

        tasks = []

        for (id, fecha, descripcion, prioridad, estado) in c:
            tasks.append(Task(id, fecha, descripcion, prioridad, estado))

    return tasks


def get_priority_state_task(priority, state):
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


def get_task_by_id(task_id):
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


def insert_task(task):
    """Inserta una nueva tarea en la base de datos
    
    Arguments:
        task {Task} -- Tarea para insertar
    """
    with closing(db.cursor()) as c:

        sql_query = "INSERT INTO agenda(fecha, descripcion, prioridad, estado) VALUES(%s, %s, %s, %s)"
        c.execute(sql_query, (task.fecha, task.descripcion, task.prioridad, task.estado))
        db.commit()


def delete_task(task_id):
    """Elimina la tarea deseada en la base de datos
    
    Arguments:
        task_id {int} -- Id de la tarea para borrar
    """
    with closing(db.cursor()) as c:
        
        sql_query = "DELETE FROM agenda WHERE id = %s"
        c.execute(sql_query, [task_id])
        db.commit()


def update_task(task):
    """Actualiza la tarea deseada en la base de datos
    
    Arguments:
        task {Task} -- Tarea para actualizar
    """
    with closing(db.cursor()) as c:
        
        sql_query = "UPDATE agenda SET fecha = %s, descripcion = %s, prioridad = %s, estado = %s WHERE id = %s"
        c.execute(sql_query, (task.fecha, task.descripcion, task.prioridad, task.estado, task.id))
        db.commit()

