from flask import Flask, render_template, url_for, flash, redirect, request
from appdev_project import app, db, bcrypt
from appdev_project.forms import (
    RegistrationForm,
    LoginForm,
    AdminLoginForm,
    AddBookForm,
    AddSectionForm,
)
from appdev_project.models import Admin, Books, Section, User
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/Browse Books")
def about():
    return "<h1>About Page</h1>"


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.user_password.data).decode(
            "utf-8"
        )
        user = User(
            user_name=form.user_name.data,
            user_email=form.user_email.data,
            user_password=hashed_password,
        )
        db.session.add(user)
        db.session.commit()
        flash(
            f"Account created for {form.user_name.data}! You will now be able to login.",
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
        user = User.query.filter_by(user_email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.user_password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Login unsuccessful. Please check email and password", "danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = AdminLoginForm()
    if form.validate_on_submit():
        if form.email.data == "admin@blog.com" and form.password.data == "password":
            flash("Welcome Admin. You have been logged in!", "success")
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Login Unsuccessful. Please ensure that you are an admin.", "danger")
    else:
        return render_template("admin_login.html", title="Admin Login", form=form)


def book_exists(book_name, author):
    """
    Check if a book with the given name and author already exists in the database.
    """
    existing_book = Books.query.filter_by(book_name=book_name, authors=author).first()
    return existing_book is not None


from flask import request

@app.route("/add_books", methods=["GET", "POST"])
def add_books():
    form = AddBookForm()

    # Get the section_id from the URL parameter
    section_id = request.args.get('section_id')

    if section_id is None:
        flash("No section specified for adding books!", "error")
        return redirect(url_for("view_sections"))

    # Get all sections
    sections = Section.query.all()

    # Prepare choices for the dropdown
    section_choices = [(section.id, section.name) for section in sections]
    form.section_id.choices = section_choices

    # Set the selected section if provided (optional)
    if section_id:
        form.section_id.data = int(section_id)

    if form.validate_on_submit():
        # Check if the book already exists
        if book_exists(form.book_name.data, form.author.data):
            flash("This book already exists!", "error")
        else:
            # Add the book to the database and associate it with the specified section
            book = Books(
                book_name=form.book_name.data,
                authors=form.author.data,
                rating=form.rating.data,
                section_id=section_id
            )
            db.session.add(book)
            db.session.commit()
            flash("Hi Admin. This book has been added successfully!", "success")
            return redirect(url_for("view_section"))  # Redirect to the view_sections page after adding the book

    return render_template("add_books.html", form=form)




@app.route("/admin_dashboard")
def admin_dashboard():
    # Logic for rendering the admin dashboard page
    return render_template("admin_dashboard.html")


@app.route("/user_dashboard")
def user_dashboard():
    return render_template("user_dashboard.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/view_books")
def view_books():
    books = Books.query.all()

    # Filter out books with empty date_issued

    # Pass the filtered books data to the template
    return render_template("view_books.html", books=books)



@app.route("/browse_books")
def browse_books():
    books = Books.query.all()
    return render_template("browse_books.html", Books=books)


@app.route("/add_section", methods=["GET", "POST"])
def add_section():
    form = AddSectionForm()
    if form.validate_on_submit():
        new_section = Section(
            name=form.section_name.data, description=form.section_description.data
        )
        print(form.section_name.data)
        print(form.section_description.data)

        # Add the new section to the database session and commit the transaction
        db.session.add(new_section)
        db.session.commit()


        # Optionally, you can redirect the user to another page or display a success message
        flash("The section has been added successfully!", "success")
        return redirect(url_for("view_section"))
    else:
        return render_template("add_section.html",form=form)
    

@app.route("/view_section", methods=["GET", "POST"])
def view_section():
    section = Section.query.all()
    return render_template("view_section.html", Section=section)
