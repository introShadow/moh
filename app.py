
from flask import Flask, request
import pymysql
import os

app = Flask(__name__)

# Настройки подключения к базе данных
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_NAME = os.getenv("DB_NAME", "moh_db")

@app.route('/')
def home():
    return {"status": "ok"}, 200

@app.route('/player_join', methods=['POST'])
def player_join():
    data = request.json
    nickname = data.get('nickname')

    if not nickname:
        return {"error": "No nickname provided"}, 400

    try:
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO players (nickname)
                VALUES (%s)
                ON DUPLICATE KEY UPDATE join_time = CURRENT_TIMESTAMP
            """
            cursor.execute(sql, (nickname,))
            connection.commit()
    except Exception as e:
        return {"error": str(e)}, 500
    finally:
        connection.close()

    return {"status": "player added"}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 5000)))
