from app import db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)

class UserForm(FlaskForm):
    username = StringField("Имя", validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField("Почта", validators=[DataRequired(), Email()])
    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Создать профиль")

class EditUserForm(FlaskForm):
    username = StringField("Имя", validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField("Почта", validators=[DataRequired(), Email()])
    password = PasswordField("Новый пароль (оставьте пустым, если не хотите менять)")
    submit = SubmitField("Сохранить изменения")
