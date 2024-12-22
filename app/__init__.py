from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)  # Исправлено на __name__
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Эта строчка отключает сигнализацию об изменении объектов внутри базы данных
app.config["SECRET_KEY"] = "your_secret_key"
db = SQLAlchemy(app)
#from app import routes

# Определите модели User и формы UserForm, EditUserForm здесь
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

@app.route("/", methods=["GET", "POST"])
def home_account():
    return render_template("home_account.html")

@app.route("/create_account", methods=["GET", "POST"])  # Исправлено на /create_account
def create_account():
    form = UserForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method="pbkdf2:sha256")
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Профиль создан!", "success")
        return redirect(url_for("home_account"))  # Исправлено на "home_account"
    return render_template("create_account.html", form=form)

@app.route("/edit_account/<int:user_id>", methods=["GET", "POST"])  # Исправлено на /edit_account/<int:user_id>
def edit_account(user_id):
    user = User.query.get(user_id)
    form = EditUserForm(obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        if form.password.data:  # Если пароль введён, обновляем его
            user.password = generate_password_hash(form.password.data, method="pbkdf2:sha256")
        db.session.commit()
        flash("Профиль обновлён!", "success")
        return redirect(url_for("home_account"))  # Исправлено на "home_account"
    return render_template("edit_account.html", form=form, user=user)

@app.route('/change_account', methods=['GET', 'POST'])
def change_account():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        return redirect(url_for('change_account', user_id=user_id))
    return render_template('change_account.html')