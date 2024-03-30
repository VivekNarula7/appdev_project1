from flask import Flask, render_template, url_for, flash, redirect, request
from appdev_project import app, db, bcrypt
from appdev_project.forms import RegistrationForm, LoginForm, AdminLoginForm
from appdev_project.models import Admin, Books, Section,User
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/Browse Books")
def about():
    return "<h1>About Page</h1>"


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.user_password.data).decode('utf-8')
        user = User(user_name = form.user_name.data, user_email= form.user_email.data, user_password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.user_name.data}! You will now be able to login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.user_password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check email and password','danger')
    return render_template('login.html',title='Login',form=form)

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = AdminLoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('Welcome Admin. You have been logged in!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Login Unsuccessful. Please ensure that you are an admin.', 'danger')
    else:
        return render_template('admin_login.html', title='Admin Login', form=form)

@app.route('/admin_dashboard/add_books', methods=['GET', 'POST'])
@login_required
def add_books():
    if request.method == 'GET':
        return render_template('view_books.html')

    if request.method == "POST":
        title = request.form['title']
        rating = request.form['rating']
        poster_url = request.form['poster_url']
        if not Books.query.filter(Books.title == title).first():
            new_book = Books(title=title, rating=rating,
                               poster_url=poster_url)
            db.session.add(new_book)
            db.session.commit()
            return render_template('view_books.html', message="Book added successfully.")
        else:
            return render_template('add_book.html', message="Book already exists in the database.")
        
@app.route('/admin_dashboard')
def admin_dashboard():
    # Logic for rendering the admin dashboard page
    return render_template('admin_dashboard.html')

@app.route('/user_dashboard')
def user_dashboard():
    return render_template('user_dashboard.html')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))