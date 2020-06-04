from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = StringField("Электропочта:", validators=[DataRequired()])
    password = PasswordField("Пароль:", validators=[DataRequired()])
    submit = SubmitField('Отправить')


class RegistrationForm(FlaskForm):
    email = StringField("Электропочта:", validators=[DataRequired()])
    password = PasswordField("Пароль:", validators=[DataRequired()])
    confirm_password = PasswordField("Повторите пароль:", validators=[DataRequired()])
    submit = SubmitField('Отправить')
