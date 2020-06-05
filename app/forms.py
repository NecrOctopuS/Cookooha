from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField("Имя:", validators=[DataRequired()])
    password = PasswordField("Пароль:", validators=[DataRequired()])
    submit = SubmitField('Отправить')


class RegistrationForm(FlaskForm):
    username = StringField("Имя:", validators=[DataRequired()])
    password = PasswordField("Пароль:", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Повторите пароль:", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Отправить')
