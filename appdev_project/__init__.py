from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
current_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# GENERATED THE SECRET KEY USING SECRETS
app.config['SECRET_KEY'] = '1da104351ce04785a9a58c6e81021b73b41046579f685f47a3915ac32ec6c9c9'

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + \
    os.path.join(current_dir, "Database_Bootcamp.sqlite3")

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# db.init_app(app)   [We should call this only once]
app.app_context().push()

from appdev_project import routes

