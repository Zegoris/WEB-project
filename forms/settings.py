from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, RadioField
from wtforms.validators import DataRequired


class SettForm(FlaskForm):
    time = RadioField('What time do you want to update the quote?',
                      choices=[('08:00', '08:00'),
                               ('10:00', '10:00'),
                               ('14:00', '14:00'),
                               ('16:00', '16:00'),
                               ('18:00', '18:00')], validators=[DataRequired()])
    type = RadioField('What type of quotes do you want to receive?',
                      choices=[('rus', 'Russian'),
                               ('for', 'Foreign'),
                               ('mix', 'Mixed')], validators=[DataRequired()])
    submit = SubmitField('Submit')