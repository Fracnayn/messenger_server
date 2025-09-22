# ... (весь код до маршрута /register) ...

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password') # Теперь мы получаем пароль
    
    # Проверяем наличие и длину имени пользователя и пароля
    if not username or len(username) < 4:
        return jsonify({"error": "Имя пользователя должно быть не менее 4 символов"}), 400
    if not password or len(password) < 4:
        return jsonify({"error": "Пароль должен быть не менее 4 символов"}), 400
        
    print(f"Запрос на регистрацию нового пользователя: {username} с паролем: {password}")
    
    # Здесь мы будем добавлять пользователя в базу данных
    
    return jsonify({"status": "success", "message": f"Пользователь {username} успешно зарегистрирован."})
