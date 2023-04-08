from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, RadioField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Login/Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat password', validators=[DataRequired()])
    time = RadioField('What time do you want to update the quote?',
                      choices=[('08', '08:00'),
                               ('10', '10:00'),
                               ('14', '14:00'),
                               ('16', '16:00'),
                               ('18', '18:00')], validators=[DataRequired()])
    type = RadioField('What type of quotes do you want to receive?',
                      choices=[('rus', 'Russian'),
                               ('for', 'Foreign'),
                               ('mix', 'Mixed')], validators=[DataRequired()])
    submit = SubmitField('Submit')