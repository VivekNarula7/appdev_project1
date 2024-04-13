from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed
from appdev_project.models import User
from flask_login import current_user


# Field name in form should match field names in user class


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                             validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                          validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_user_name(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That username is taken. Please choose a different one.')

    def validate_user_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class AdminLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    remember = BooleanField('Remember Me')


class AddBookForm(FlaskForm):
    book_name = StringField('Book Name', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    rating = IntegerField('Rating', validators=[DataRequired()])
    section_id = SelectField('Section', coerce=int, choices=[], validators=[DataRequired()])
    submit = SubmitField('Add Book')


class AddSectionForm(FlaskForm):
    section_name = StringField('Genre', validators=[DataRequired()])
    section_description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Add Section')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')
