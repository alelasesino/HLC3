
import datetime


def format_date(date):
    """Funcion que convierte la fecha con formato %Y-%m-%d en
    una fecha con formato %d-%m-%Y
    
    Arguments:
        date {datetime} -- Fecha con formato %Y-%m-%d
    
    Returns:
        datetime -- Fecha con formato %d-%m-%Y
    """
    d = datetime.datetime.strptime(str(date), '%Y-%m-%d')
    return d.strptime(d.strftime('%d-%m-%Y'), '%d-%m-%Y')


def string_state(id_state, plural = False):
    """Devuelve la cadena que reprensenta el id pasado por parmetro,
    permite que la cadena devuelta sea en plural, excepto el estado en proceso
    
    Arguments:
        id_state {int} -- Id de la tarea
    
    Keyword Arguments:
        plural {bool} -- Cadena del estado de la tarea en plural (default: {False})
    
    Returns:
        str -- Cadena con el estado de la tarea
    """
    STATES = ["Pendiente", "En proceso", "Completada"]

    state = STATES[id_state]

    if plural:
        state += ("s" if id_state != 1 else "") #EL ESTADO 'En proceso' NUNCA EL PLURAL

    return state

