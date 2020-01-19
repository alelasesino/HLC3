
import datetime
from Ejercicio04.utils import format_date
from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField, IntegerField, PasswordField, BooleanField, TextField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired, ValidationError
from Ejercicio04.database import get_user_by_username
from Ejercicio04.models import User 

PrioritySelectField = SelectField(choices=[(i, i) for i in range(6)], coerce=int)
StateSelectField = SelectField(choices=[(0, 'Pendiente'), (1, 'En proceso'), (2, 'Completada')], coerce=int)

class TaskForm(FlaskForm):
    """Formulario que permite crear y modificar las tareas
    """
    fecha = DateField('Fecha', validators=[InputRequired(message="La fecha es requerida")])
    descripcion = TextAreaField('Descripcion', validators=[InputRequired(message="La descripcion es requerida")], render_kw={"placeholder": "Descripcion..."})
    prioridad = PrioritySelectField
    estado = StateSelectField

    def __init__(self, update, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update = update
        if not self.fecha.data:
            self.fecha.data = datetime.date.today()

    def validate_fecha(self, field):
        past = format_date(field.data)
        past_date = datetime.datetime(past.year, past.month, past.day)
        present_date = datetime.datetime.now() - datetime.timedelta(days=1)
        
        if past_date < present_date and not self.update:
            raise ValidationError("La fecha no puede ser anterior a la actual")


class SelectTaskForm(FlaskForm):
    """Formulario que permite seleccionar una tarea por su id
    """
    id = IntegerField('ID de la tarea', validators=[InputRequired(message="El ID de la tarea es requerida")], render_kw={"placeholder": "ID de la tarea..."})

    def __init__(self, task_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task_list = task_list    

    def validate_id(self, field):
        if not any(task.id == field.data for task in self.task_list):
            raise ValidationError("El ID de la tarea no existe")


class TaskListForm(FlaskForm):
    """Formulario que permite filtrar las tareas por estado y por prioridad
    """
    prioridad = PrioritySelectField
    estado = StateSelectField


class LoginForm(FlaskForm):
    """Formulario que permite iniciar sesion al usuario
    """
    username = TextField('Usuario', validators=[InputRequired(message="El usuario es requerido")], render_kw={"placeholder": "Usuario..."})
    password = PasswordField('Contraseña', validators=[InputRequired(message="La contraseña es requerida")], render_kw={"placeholder": "Contraseña..."})
    remember = BooleanField("Recordar este equipo")
    user: User = None

    def validate_username(self, field):
        self.user = get_user_by_username(self.username.data)

        if self.user == None:
            raise ValidationError("Nombre de usuario no existe")

        if self.user.username != self.username.data:
            raise ValidationError("Nombre de usuario incorrecto")
            

    def validate_password(self, field):

        if self.user != None:
            if self.user.password != self.password.data:
                raise ValidationError("Contraseña incorrecta")


class RegisterForm(FlaskForm):
    """Formulario que permite registrar un usuario
    """
    username = TextField('Usuario', validators=[InputRequired(message="El usuario es requerido")], render_kw={"placeholder": "Usuario..."})
    password = PasswordField('Contraseña', validators=[InputRequired(message="La contraseña es requerida")], render_kw={"placeholder": "Contraseña..."})
    nickname = TextField('Nombre', validators=[InputRequired(message="El nombre es requerido")], render_kw={"placeholder": "Nombre..."})

    def validate_username(self, field):
        user: User = get_user_by_username(self.username.data)
        if user != None:
            raise ValidationError("El nombre de usuario ya existe")

