from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, RadioField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Login/Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat password', validators=[DataRequired()])
    type = RadioField('What type of quotes do you want to receive?',
                      choices=[('rus', 'Russian'),
                               ('for', 'Foreign'),
                               ('mix', 'Mixed')], validators=[DataRequired()])
    submit = SubmitField('Submit')