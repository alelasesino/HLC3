
from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = "KeySecret"

Bootstrap(app)

import Ejercicio03.views
