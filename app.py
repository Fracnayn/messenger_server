from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/send_message": {"origins": "*", "methods": ["POST"]}, r"/register": {"origins": "*", "methods": ["POST"]}})

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
        return {"status": "success", "message": "Сообщение получено"}
    return {"status": "error", "message": "Неверные данные"}, 400

# НОВЫЙ МАРШРУТ для регистрации
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    
    if not username:
        return jsonify({"error": "Имя пользователя обязательно"}), 400
        
    print(f"Запрос на регистрацию нового пользователя: {username}")
    
    # Здесь мы будем добавлять пользователя в базу данных
    
    return jsonify({"status": "success", "message": f"Пользователь {username} успешно зарегистрирован."})
