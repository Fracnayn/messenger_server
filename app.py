from flask import Flask, request

app = Flask(__name__)

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    if data:
        print(f"Получено сообщение: {data.get('text')}")
        return {"status": "success", "message": "Сообщение получено"}
    return {"status": "error", "message": "Неверные данные"}, 400

if __name__ == '__main__':
    app.run(port=5000, debug=True)