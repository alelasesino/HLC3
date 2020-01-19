
from datetime import datetime
from Ejercicio03.utils import string_state


class Task:
    """Modelo de una tarea
    """
    def __init__(self, id:int, fecha:datetime, descripcion:str, prioridad:int, estado:int):
        self.id = id
        self.fecha = fecha
        self.descripcion = descripcion
        self.prioridad = prioridad
        self.estado = estado
        self.estadostr = string_state(estado)

    @classmethod
    def new_task(cls):
        return cls(-1, datetime.now(), '', 0, 0)


class User:
    """Modelo de un usuario
    """
    def __init__(self, username:str, password:str, nickname:str, permission:str):
        self.username = username
        self.password = password
        self.nickname = nickname
        self.permission = permission

    @classmethod
    def new_user(cls):
        return cls("", "", "", "")
