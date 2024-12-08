from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

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

@app.route('/add_score', methods=['POST'])
def add_score():
    data = request.json
    game = data.get("game")
    score = data.get("score")
    if game and score is not None:
        scores[game].append(score)
        return jsonify({"status": "success", "scores": scores[game]})
    return jsonify({"status": "error"}), 400

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
def reaction_time_test():
    return render_template('components/ReactionTimeTest.html')

@app.route('/test')
def test():
    return render_template('components/Test.html')

if __name__ == '__main__':
    app.run(debug=True)
