from flask import Flask, request
import os
import requests

app = Flask(__name__)

# Конфигурация API
API_URL = os.getenv("REMOTE_API_URL", "https://introhub.top/api/player_join.php")
API_KEY = os.getenv("REMOTE_API_KEY", "MijhGA982hhJkalPd8JA8sJ9da")  # Заменишь в Render

@app.route('/')
def home():
    return {"status": "ok"}, 200

@app.route('/player_join', methods=['POST'])
def player_join():
    data = request.json
    nickname = data.get("nickname")

    if not nickname:
        return {"error": "No nickname provided"}, 400

    # Подготовка данных и отправка запроса на твой сайт
    try:
        payload = {
            "nickname": nickname,
            "api_key": API_KEY
        }
        response = requests.post(API_URL, data=payload, timeout=5)
        return response.json(), response.status_code
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 5000)))
