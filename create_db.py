from app import db, app

with app.app_context():  # Создаём контекст приложения
    db.create_all()  # Создаёт базы данных и таблицы