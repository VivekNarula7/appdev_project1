from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from appdev_project.models import User

# Field name in form should match field names in user class


class RegistrationForm(FlaskForm):
    user_name = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    user_email = StringField('Email',
                        validators=[DataRequired(), Email()])
    user_password = PasswordField('Password', validators=[DataRequired()])
    confirm_user_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('user_password')])
    submit = SubmitField('Sign Up')

    def validate_user_name(self, user_name):
        user = User.query.filter_by(user_name=user_name.data).first()
        if user:
            raise ValidationError(
                'That username is taken. Please choose a different one.')

    def validate_user_email(self, user_email):
        user = User.query.filter_by(user_email=user_email.data).first()
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
    submit = SubmitField('Add Book')

class AddSectionForm(FlaskForm):
    section_name = StringField('Genre', validators=[DataRequired()])
    section_description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Add Section')
