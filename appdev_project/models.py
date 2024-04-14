from datetime import datetime
from appdev_project import db, login_manager, bcrypt
from flask_login import UserMixin
from flask_bcrypt import check_password_hash


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@login_manager.user_loader
def load_admin(id):
    return Admin.query.get(int(id))


class Admin(UserMixin, db.Model):
    __tablename__ = "Admin"
    id = db.Column(db.Integer, primary_key=True)
    admin_name = db.Column(db.String(20), unique=True, nullable=False)
    admin_email = db.Column(db.String(120), unique=True, nullable=False)
    admin_password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    def check_password(self, password):
        return check_password_hash(self.admin_password, password)

    def __repr__(self):
        return f"Admin(id={self.id}, admin_name='{self.admin_name}', admin_email='{self.admin_email}')"


class User(db.Model, UserMixin):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User(id={self.id}, username='{self.username}', email='{self.email}',image_file='{self.image_file}')"


class Books(db.Model):
    __tablename__ = "Books"
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(255), nullable=True)  # stores the path to the pdf file
    authors = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey("Section.id"), nullable=False)
    section = db.relationship("Section", backref=db.backref("books", lazy=True))
    link = db.Column(db.String(255))  # Add link column

    def __repr__(self):
        return f"Book(id={self.id}, book_name='{self.book_name}')"


class Section(db.Model):
    __tablename__ = "Section"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"Section(id={self.id}, name='{self.name}', date_created='{self.date_created}')"
