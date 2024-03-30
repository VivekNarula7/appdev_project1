from datetime import datetime
from appdev_project import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Admin(db.Model):
    __tablename__ = "Admin"
    id = db.Column(db.Integer, primary_key=True)
    admin_name = db.Column(db.String(20), unique=True, nullable=False)
    admin_email = db.Column(db.String(120), unique=True, nullable=False)
    admin_password = db.Column(db.String(60), nullable=False)

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
    book_name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_issued = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    authors = db.Column(db.String(100), nullable=False)
    return_date = db.Column(db.DateTime, nullable=True)
    rating = db.Column(db.Integer, nullable = False)
    section_id = db.Column(db.Integer, db.ForeignKey("Section.id"), nullable=False)
    section = db.relationship("Section", backref=db.backref("books", lazy=True))

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


# class RentedBooks(db.Model):
#     __tablename__ = "RentedBooks"
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
#     book_id = db.Column(db.Integer, db.ForeignKey('Books.id'), nullable=False)
#     date_issued = db.Column(db.DateTime, nullable=False,
#                             default=datetime.utcnow)
#     return_date = db.Column(db.DateTime, nullable=True)

#     user = db.relationship("User", backref="rented_books")
#     book = db.relationship("Book", backref="rented_users")

#     def __repr__(self):
#         return f"RentedBooks(id={self.id}, user_id={self.user_id}, book_id={self.book_id}, date_issued={self.date_issued}, return_date={self.return_date})"
