
from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = "OfUJnnclWc7iAWap1qsr"

Bootstrap(app)

import Ejercicio02.views
