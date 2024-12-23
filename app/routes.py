from flask import render_template, redirect, url_for, flash, request
from app import app, db
from app.models import User
from app.forms import UserForm
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    form = UserForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method="pbkdf2:sha256")
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Пользователь создан!', 'success')
        return redirect(url_for('home'))
    return render_template('create.html', form=form)

@app.route('/edit/<int:user_id>', methods=['GET', 'POST'], endpoint="edit")
def edit(user_id):
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        db.session.commit()
        flash('Данные пользователя обновлены!', 'success')
        return redirect(url_for('home'))
    return render_template('edit.html', form=form, user=user)

@app.route('/search', methods=['GET', 'POST'])
def search():
    username = request.args.get('username')
    user = User.query.filter_by(username=username).first()
    if user:
        return redirect(url_for('edit', user_id=user.id))
    flash('Пользователь не найден!', 'danger')
    return redirect(url_for('home'))