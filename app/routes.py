from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from app import models
from app.models import UserForm, EditUserForm, User

app = Flask(__name__)  # Исправлено на __name__
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"  # Раскомментировано
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Эта строчка отключает сигнализацию об изменении объектов внутри базы данных
app.config["SECRET_KEY"] = "your_secret_key"  # Раскомментировано
db = SQLAlchemy(app)  # Инициализация базы данных

@app.route("/")
def home_account():
    return render_template("home_account.html")

@app.route("/create_account", methods=["GET", "POST"])  # Исправлено на /create_account
def create_account():
    form = UserForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method="sha256")
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Профиль создан!", "success")
        return redirect(url_for("create_account", user_id=new_user.id))
    return render_template("create_account.html", form=form)

@app.route("/edit_account/<int:user_id>", methods=["GET", "POST"])  # Исправлено на /edit_account/<int:user_id>
def edit_account(user_id):
    user = User.query.get_or_404(user_id)
    form = EditUserForm(obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        if form.password.data:  # Если пароль введён, обновляем его
            user.password = generate_password_hash(form.password.data, method="sha256")
        db.session.commit()
        flash("Профиль обновлён!", "success")
        return redirect(url_for("edit_account", user_id=user.id))
    return render_template("edit_account.html", form=form, user=user)