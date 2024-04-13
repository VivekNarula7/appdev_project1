from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
import os
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user, login_required, UserMixin
from flask_admin import Admin, AdminIndexView, BaseView, expose, form
from wtforms.validators import ValidationError

current_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# GENERATED THE SECRET KEY USING SECRETS
app.config['SECRET_KEY'] = '1da104351ce04785a9a58c6e81021b73b41046579f685f47a3915ac32ec6c9c9'

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + \
                                        os.path.join(current_dir, "Database_Bootcamp.db")

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')

login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

app.app_context().push()

from appdev_project import routes
from appdev_project.models import User, Books, Section
from flask_admin.contrib.sqla import ModelView

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Section, db.session))

from flask_admin.form import Select2Widget


class CustomAdminView(ModelView):
    form_columns = ('book_name', 'content', 'authors', 'rating', 'section', 'link')
    column_list = ["book_name", "content", "authors", "rating", "section_name", 'link']
    # Optionally, you can customize the form field for the section selection
    form_widget_args = {
        'section': {
            'widget': Select2Widget()
        }
    }

    def on_model_change(self, form, model, is_created):
        if is_created:  # Check if it's a new book being added
            # Check if a book with the same name and author already exists
            existing_book = model.query.filter_by(book_name=model.book_name, authors=model.authors).first()
            if existing_book and existing_book.id != model.id:
                raise ValidationError("A book with the same name and author already exists!")
        super().on_model_change(form, model, is_created)


# Register the custom admin view
admin.add_view(CustomAdminView(Books, db.session))
