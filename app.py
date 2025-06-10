from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Используем PostgreSQL, если доступна, иначе SQLite (для локальной разработки)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    "DATABASE_URL", "sqlite:///tmp/messages.db"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)

# Инициализация базы данных
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return "API is running!"

@app.route('/delete-message', methods=['POST'])
def delete_message():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "Text is required"}), 400

    text = data['text']
    message = Message.query.filter_by(text=text).first()
    if message:
        db.session.delete(message)
        db.session.commit()
        return jsonify({"status": "deleted"}), 200
    else:
        return jsonify({"error": "Message not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
