import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from passlib.context import CryptContext

# Настройка хеширования паролей
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Инициализация приложения и базы данных
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Проверка, существует ли файл базы данных
if os.path.exists('users.db'):
    os.remove('users.db')
    print("Старая база данных удалена. Создаем новую.")

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

# Модель для хранения информации о дружбе
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

    hashed_password = hash_password(password)
    new_user = User(username=username, password=hashed_password)
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

    user = session.query(User).filter_by(username=username).first()

    if user and verify_password(password, user.password):
        print(f"Пользователь {username} успешно вошел в систему.")
        return jsonify({"status": "success", "message": "Вход выполнен успешно."}), 200
    else:
        return jsonify({"error": "Неправильное имя пользователя или пароль"}), 401

# Маршрут для поиска пользователя
@app.route('/search_user', methods=['POST'])
def search_user():
    data = request.json
    username = data.get('username')

    user = session.query(User).filter_by(username=username).first()

    if user:
        return jsonify({"exists": True, "username": user.username}), 200
    else:
        return jsonify({"exists": False}), 404

# НОВЫЙ МАРШРУТ для добавления друга
@app.route('/add_friend', methods=['POST'])
def add_friend():
    data = request.json
    user_id = data.get('user_id')
    friend_id = data.get('friend_id')

    # Проверяем, существует ли уже дружба между этими пользователями
    existing_friendship = session.query(Friendship).filter_by(user_id=user_id, friend_id=friend_id).first()
    if existing_friendship:
        return jsonify({"status": "error", "message": "Вы уже друзья"}), 409

    # Создаем запись о дружбе в двух направлениях
    friendship1 = Friendship(user_id=user_id, friend_id=friend_id)
    friendship2 = Friendship(user_id=friend_id, friend_id=user_id)
    session.add_all([friendship1, friendship2])
    session.commit()

    return jsonify({"status": "success", "message": "Друг успешно добавлен"}), 200

if __name__ == '__main__':
    app.run(debug=True)import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from passlib.context import CryptContext

# Настройка хеширования паролей
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Инициализация приложения и базы данных
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Проверка, существует ли файл базы данных
if os.path.exists('users.db'):
    os.remove('users.db')
    print("Старая база данных удалена. Создаем новую.")

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

# Модель для хранения информации о дружбе
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

    hashed_password = hash_password(password)
    new_user = User(username=username, password=hashed_password)
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

    user = session.query(User).filter_by(username=username).first()

    if user and verify_password(password, user.password):
        print(f"Пользователь {username} успешно вошел в систему.")
        return jsonify({"status": "success", "message": "Вход выполнен успешно."}), 200
    else:
        return jsonify({"error": "Неправильное имя пользователя или пароль"}), 401

# Маршрут для поиска пользователя
@app.route('/search_user', methods=['POST'])
def search_user():
    data = request.json
    username = data.get('username')

    user = session.query(User).filter_by(username=username).first()

    if user:
        return jsonify({"exists": True, "username": user.username}), 200
    else:
        return jsonify({"exists": False}), 404

# НОВЫЙ МАРШРУТ для добавления друга
@app.route('/add_friend', methods=['POST'])
def add_friend():
    data = request.json
    user_id = data.get('user_id')
    friend_id = data.get('friend_id')

    # Проверяем, существует ли уже дружба между этими пользователями
    existing_friendship = session.query(Friendship).filter_by(user_id=user_id, friend_id=friend_id).first()
    if existing_friendship:
        return jsonify({"status": "error", "message": "Вы уже друзья"}), 409

    # Создаем запись о дружбе в двух направлениях
    friendship1 = Friendship(user_id=user_id, friend_id=friend_id)
    friendship2 = Friendship(user_id=friend_id, friend_id=user_id)
    session.add_all([friendship1, friendship2])
    session.commit()

    return jsonify({"status": "success", "message": "Друг успешно добавлен"}), 200

if __name__ == '__main__':
    app.run(debug=True)
