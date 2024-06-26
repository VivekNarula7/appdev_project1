from flask import Flask, render_template, url_for, flash, redirect, request, abort
from appdev_project import app, db, bcrypt
from appdev_project.forms import (
    RegistrationForm,
    LoginForm,
    AdminLoginForm,
    AddBookForm,
    AddSectionForm,
    UpdateAccountForm,
)
from appdev_project.models import User, Books, Section, Admin
from flask_login import login_user, current_user, logout_user, login_required, LoginManager, UserMixin
# from flask_admin.contrib.sqla import ModelView
from wtforms.validators import ValidationError
import secrets, os
from PIL import Image
from flask_bcrypt import check_password_hash


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/BrowseBooks")
def about():
    return "<h1>About Page</h1>"


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(
            f"Account created for {form.username.data}! You will now be able to login.",
            "success",
        )
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Login unsuccessful. Please check email and password", "danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/user_dashboard")
@login_required
def user_dashboard():
    return render_template("user_dashboard.html")


@app.route("/browse-books")
def browse_books():
    books = Books.query.all()
    return render_template("browse_books.html", books=books)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        # Redirect to admin dashboard if admin is already logged in
        return redirect(url_for('admin_dashboard'))

    form = AdminLoginForm()  # Assuming you have a form for admin login
    if form.validate_on_submit():
        admin = Admin.query.filter_by(admin_email=form.email.data).first()
        if admin and admin.admin_password == form.password.data:
            login_user(admin)  # Log in the admin user
            flash('Logged in successfully.', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('admin_login.html', form=form)


@app.route("/admin_dashboard")
@login_required
def admin_dashboard():
    # Logic for rendering the admin dashboard page
    return render_template("admin_dashboard.html")


def book_exists(book_name, author):
    existing_book = Books.query.filter_by(book_name=book_name, authors=author).first()
    return existing_book is not None


@app.route("/add_books", methods=["GET", "POST"])
def add_books():
    form = AddBookForm()

    # Populate choices for section_id in the form
    form.section_id.choices = [(section.id, section.name) for section in Section.query.all()]

    if form.validate_on_submit():
        # Initialize pdf_path_relative variable
        pdf_path_relative = None

        # Handle file upload
        pdf_file = form.content.data
        if pdf_file:
            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(pdf_file.filename)
            pdf_fn = random_hex + f_ext
            pdf_path = os.path.join(app.root_path, 'static/books', pdf_fn)
            pdf_file.save(pdf_path)
            pdf_path_relative = os.path.join('books', pdf_fn)  # Relative path for storing in the database

        # Check if the book already exists
        if book_exists(form.book_name.data, form.author.data):
            flash("This book already exists!", "error")
        else:
            # Add the book to the database
            book = Books(
                book_name=form.book_name.data,
                authors=form.author.data,
                rating=form.rating.data,
                content=pdf_path_relative,  # Save the relative path to the PDF file if uploaded
                link=form.link.data,
                section_id=form.section_id.data  # Get section_id from the form
            )
            db.session.add(book)
            db.session.commit()
            flash("Hi Admin. This book has been added successfully!", "success")
            return redirect(url_for("view_section"))  # Redirect to the view_sections page after adding the book

    return render_template("add_books.html", form=form)


@app.route("/view_books")
def view_books():
    books = Books.query.all()
    return render_template("view_books.html", books=books)


@app.route("/add_section", methods=["GET", "POST"])
def add_section():
    form = AddSectionForm()
    if form.validate_on_submit():
        new_section = Section(
            name=form.section_name.data, description=form.section_description.data
        )
        # Add the new section to the database session and commit the transaction
        db.session.add(new_section)
        db.session.commit()

        # Optionally, you can redirect the user to another page or display a success message
        flash("The section has been added successfully!", "success")
        return redirect(url_for("view_section"))
    else:
        return render_template("add_section.html", form=form)


@app.route("/view_section", methods=["GET", "POST"])
def view_section():
    section = Section.query.all()
    return render_template("view_section.html", Section=section)


@app.route("/book/<int:book_id>")
def book(book_id):
    # Query the database for the selected book based on its ID
    book = Books.query.get_or_404(book_id)
    # Render the book page template and pass the book data to it
    return render_template("book.html", book=book)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@app.route("/view_pdf/<int:book_id>")
def view_pdf(book_id):
    # Retrieve the book from the database based on the book_id
    book = Books.query.get(book_id)
    if not book:
        abort(404)  # Return 404 error if book not found

    # Pass the PDF content path to the template
    pdf_path = book.content  # Assuming book.content contains the path to the PDF file
    return render_template("view_pdf.html", pdf_path=pdf_path)
