from flask import Flask, request
from flask_cors import CORS # Добавлена новая строка

app = Flask(__name__)
CORS(app) # Добавлена новая строка, чтобы включить CORS

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
