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

GAME_RECORDS = {
    "shootTest": {"label": "Shoot Test", "unit": "shots", "best": "max"},
    "clicksPerSecond": {"label": "Click Speed", "unit": "CPS", "best": "max"},
    "recenter": {"label": "Re-center", "unit": "points", "best": "max"},
    "holdBall": {"label": "Hold Ball", "unit": "points", "best": "max"},
    "horizontalHold": {"label": "Horizontal Hold", "unit": "points", "best": "max"},
    "verticalHold": {"label": "Vertical Hold", "unit": "points", "best": "max"},
    "reactionTimeTest": {"label": "Reaction Time", "unit": "ms", "best": "min"},
}

BLOCKED_IPS = set()

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

def parse_score(value: str):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None

def format_record(game: str, value: float) -> str:
    unit = GAME_RECORDS[game]["unit"]
    if unit == "CPS":
        return f"{value:.2f} CPS"
    if unit == "ms":
        return f"{value:.0f} ms"
    return f"{value:.0f} {unit}"

def get_best_records():
    records = {}
    for game, settings in GAME_RECORDS.items():
        parsed_scores = []
        for encrypted_score in scores.get(game, []):
            try:
                parsed = parse_score(decrypt_data(encrypted_score))
            except Exception:
                parsed = None
            if parsed is not None:
                parsed_scores.append(parsed)

        best_score = None
        if parsed_scores:
            best_score = min(parsed_scores) if settings["best"] == "min" else max(parsed_scores)

        records[game] = {
            "label": settings["label"],
            "unit": settings["unit"],
            "direction": settings["best"],
            "attempts": len(parsed_scores),
            "best": best_score,
            "display": format_record(game, best_score) if best_score is not None else None,
        }
    return records

@app.route('/add_score', methods=['POST'])
def add_score():
    data = request.get_json(silent=True) or {}
    game = data.get("game")
    parsed_score = parse_score(data.get("score"))
    if game not in GAME_RECORDS:
        return jsonify({"status": "error", "message": "Invalid game"}), 400
    if parsed_score is None:
        return jsonify({"status": "error", "message": "Invalid score"}), 400

    encrypted_score = encrypt_data(str(parsed_score))
    scores[game].append(encrypted_score)
    return jsonify({"status": "success", "scores": scores[game]})

@app.route('/view_scores', methods=['GET'])
@check_ip
@check_role('admin')
def view_scores():
    decrypted_scores = {game: [decrypt_data(score) for score in score_list] 
                        for game, score_list in scores.items()}
    return jsonify({"scores": decrypted_scores})

@app.route('/best_scores', methods=['GET'])
def best_scores():
    return jsonify({"records": get_best_records()})

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
    return render_template('components/ReCenter.html')

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
def reaction_time_test():
    return render_template('components/ReactionTimeTest.html')

@app.route('/scoreboard')
def scoreboard():
    return render_template('components/Scoreboard.html')

@app.route('/api/your-endpoint', methods=['GET'])
@check_ip
def your_route():
    return jsonify({'data': 'your response'})

if __name__ == '__main__':
    app.run(debug=True)
