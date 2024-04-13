from datetime import datetime
from appdev_project import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Admin(UserMixin, db.Model):
    __tablename__ = "Admin"
    id = db.Column(db.Integer, primary_key=True)
    admin_name = db.Column(db.String(20), unique=True, nullable=False)
    admin_email = db.Column(db.String(120), unique=True, nullable=False)
    admin_password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Admin(id={self.id}, admin_name='{self.admin_name}', admin_email='{self.admin_email}')"


class User(db.Model, UserMixin):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), unique=True, nullable=False)
    user_email = db.Column(db.String(120), unique=True, nullable=False)
    user_password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User(id={self.id}, user_name='{self.user_name}', user_email='{self.user_email}')"


class Books(db.Model):
    __tablename__ = "Books"
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(100))
    content = db.Column(db.Text)
    authors = db.Column(db.String(100))
    rating = db.Column(db.Integer)
    section_name = db.Column(db.String(100), db.ForeignKey("Section.name"))
    section = db.relationship("Section", back_populates="books")
    link = db.Column(db.String(255))

    def __repr__(self):
        return f"Book(id={self.id}, book_name='{self.book_name}', authors='{self.authors}', rating={self.rating}, link='{self.link}')"


class Section(db.Model):
    __tablename__ = "Section"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=True)
    books = db.relationship("Books", back_populates="section")

    def __repr__(self):
        return f'{self.name}'
