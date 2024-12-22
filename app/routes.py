from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from app import models
from app.models import UserForm, EditUserForm, User

# app = Flask(__name__)  # Исправлено на __name__
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"  # Раскомментировано
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Эта строчка отключает сигнализацию об изменении объектов внутри базы данных
# app.config["SECRET_KEY"] = "your_secret_key"  # Раскомментировано
# db = SQLAlchemy(app)  # Инициализация базы данных



