from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# Инициализация приложения и базы данных
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Настройка базы данных SQLite
engine = create_engine('sqlite:///users.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Модель пользователя
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    def __repr__(self):
        return f"<User(username='{self.username}')>"

# НОВАЯ МОДЕЛЬ для хранения информации о дружбе
class Friendship(Base):
    __tablename__ = 'friendships'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    friend_id = Column(Integer, ForeignKey('users.id'), nullable=False)

# Создание всех таблиц
Base.metadata.create_all(engine)

# Маршрут для главной страницы
@app.route('/')
def home():
    return "Сервер мессенджера Fracnayn запущен!"

# Маршрут для отправки сообщений
@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    if data:
        print(f"Получено сообщение: {data.get('text')}")
        return jsonify({"status": "success", "message": "Сообщение получено"})
    return jsonify({"status": "error", "message": "Неверные данные"}), 400

# Маршрут для регистрации
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or len(username) < 4:
        return jsonify({"error": "Имя пользователя должно быть не менее 4 символов"}), 400
    if not password or len(password) < 4:
        return jsonify({"error": "Пароль должен быть не менее 4 символов"}), 400

    existing_user = session.query(User).filter_by(username=username).first()
    if existing_user:
        return jsonify({"error": "Пользователь с таким именем уже существует"}), 409

    new_user = User(username=username, password=password)
    session.add(new_user)
    session.commit()

    print(f"Зарегистрирован новый пользователь: {username}")
    return jsonify({"status": "success", "message": f"Пользователь {username} успешно зарегистрирован."}), 200

# Маршрут для входа
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = session.query(User).filter_by(username=username, password=password).first()

    if user:
        print(f"Пользователь {username} успешно вошел в систему.")
        return jsonify({"status": "success", "message": "Вход выполнен успешно."}), 200
    else:
        return jsonify({"error": "Неправильное имя пользователя или пароль"}), 401

# НОВЫЙ МАРШРУТ для поиска пользователя
@app.route('/search_user', methods=['POST'])
def search_user():
    data = request.json
    username = data.get('username')
    
    user = session.query(User).filter_by(username=username).first()
    
    if user:
        return jsonify({"exists": True, "username": user.username}), 200
    else:
        return jsonify({"exists": False}), 404 # Код 404 Not Found

if __name__ == '__main__':
    app.run(debug=True)
