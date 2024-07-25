from flask import Flask, request, jsonify, make_response, render_template
from akinator_python import Akinator
import uuid

app = Flask(__name__, template_folder='.')

# Global dictionary to store Akinator instances and game states for multiple users
user_games = {}

def get_user_token():
    return request.args.get('user_token') or request.cookies.get('user_token')

@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/start', methods=['GET'])
def start_game():
    try:
        user_token = str(uuid.uuid4())
        akinator = Akinator(lang="id")
        user_games[user_token] = akinator
        question = akinator.start_game()

        response = make_response(jsonify({"user_token": user_token, "question": question}))
        response.set_cookie('user_token', user_token)
        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/answer', methods=['GET'])
def post_answer():
    try:
        answer = request.args.get('q')
        user_token = get_user_token()

        if not user_token or user_token not in user_games:
            return jsonify({"error": "No game in progress"}), 400

        if answer in ["y", "n", "idk", "p", "pn"]:
            akinator = user_games[user_token]
            akinator.post_answer(answer)
            if akinator.answer_id:
                return jsonify({
                    "name": akinator.name,
                    "description": akinator.description
                })
            else:
                return jsonify({"user_token": user_token, "question": akinator.question})
        else:
            return jsonify({"error": "Invalid answer"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/back', methods=['POST'])
def go_back():
    try:
        user_token = get_user_token()

        if not user_token or user_token not in user_games:
            return jsonify({"error": "No game in progress"}), 400

        akinator = user_games[user_token]
        akinator.go_back()
        return jsonify({"user_token": user_token, "question": akinator.question})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/exclude', methods=['POST'])
def exclude():
    try:
        user_token = get_user_token()

        if not user_token or user_token not in user_games:
            return jsonify({"error": "No game in progress"}), 400

        akinator = user_games[user_token]
        akinator.exclude()
        return jsonify({"user_token": user_token, "question": akinator.question})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/progress', methods=['GET'])
def progress():
    try:
        user_token = get_user_token()

        if not user_token or user_token not in user_games:
            return jsonify({"error": "No game in progress"}), 400

        akinator = user_games[user_token]
        progression = akinator.progression
        step = akinator.step
        return jsonify({"user_token": user_token, "progression": progression, "step": step})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
