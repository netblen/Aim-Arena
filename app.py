import os
from flask import Flask, jsonify, render_template, request
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from functools import wraps

app = Flask(__name__)
load_dotenv()

encryption_key = os.getenv('ENCRYPTION_KEY')
if not encryption_key:
    encryption_key = Fernet.generate_key()
    with open('.env', 'w') as f:
        f.write(f'ENCRYPTION_KEY={encryption_key.decode()}')
fernet = Fernet(encryption_key.encode())

scores = {
    "shootTest": [],
    "clicksPerSecond": [],
    "recenter": [],
    "holdBall": [],
    "horizontalHold": [],
    "verticalHold": [],
    "reactionTimeTest": [],
    "test": []
}

BLOCKED_IPS = {'127.0.0.1'}

USERS = {
    'admin_user': {'password': 'adminpass', 'role': 'admin'},
    'regular_user': {'password': 'userpass', 'role': 'user'}
}

def check_ip(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if request.remote_addr in BLOCKED_IPS:
            return jsonify({'error': 'blocked'}), 403
        return f(*args, **kwargs)
    return wrapper

def check_role(required_role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user = request.args.get('user') 
            if user not in USERS:
                return jsonify({'error': 'Unauthorized access'}), 403
            if USERS[user]['role'] != required_role:
                return jsonify({'error': 'Insufficient permissions'}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator

def encrypt_data(data: str) -> str:
    """Encrypt a string."""
    return fernet.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data: str) -> str:
    """Decrypt an encrypted string."""
    return fernet.decrypt(encrypted_data.encode()).decode()

@app.route('/add_score', methods=['POST'])
@check_ip 
@check_role('admin') 
def add_score():
    data = request.json
    game = data.get("game")
    score = data.get("score")
    if game and score is not None:
        encrypted_score = encrypt_data(str(score))
        scores[game].append(encrypted_score)
        return jsonify({"status": "success", "scores": scores[game]})
    return jsonify({"status": "error"}), 400

@app.route('/view_scores', methods=['GET'])
@check_ip
@check_role('admin')
def view_scores():
    decrypted_scores = {game: [decrypt_data(score) for score in score_list] 
                        for game, score_list in scores.items()}
    return jsonify({"scores": decrypted_scores})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('components/Home.html')

@app.route('/clicks-per-second')
def clicks_per_second():
    return render_template('components/ClicksPerSecond.html')

@app.route('/shoot-test')
def shoot_test():
    return render_template('components/ShootTest.html')

@app.route('/recenter')
def recenter():
    return render_template('components/Recenter.html')

@app.route('/hold-ball')
def hold_ball():
    return render_template('components/HoldBall.html')

@app.route('/horizontal-hold')
def horizontal_hold():
    return render_template('components/HorizontalHold.html')

@app.route('/vertical-hold')
def vertical_hold():
    return render_template('components/VerticalHold.html')

@app.route('/reaction-time-test')
@check_ip
@check_role('user')
def reaction_time_test():
    return render_template('components/ReactionTimeTest.html')

@app.route('/api/your-endpoint', methods=['GET'])
@check_ip
def your_route():
    return jsonify({'data': 'your response'})

if __name__ == '__main__':
    app.run(debug=True)
