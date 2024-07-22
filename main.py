from flask import Flask, request, jsonify, session
from akinator_python import Akinator
import os

app = Flask(__name__, template_folder='.')

app.secret_key = os.urandom(24)

@app.route('/')
def welcome():
    return render_template('index.html')
  
@app.route('/start', methods=['GET'])
def start_game():
    try:
        session['akinator'] = Akinator(lang="id")
        question = session['akinator'].start_game()
        return jsonify({"question": question}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/answer', methods=['GET'])
def post_answer():
    try:
        answer = request.args.get('q')
        if answer in ["y", "n", "idk", "p", "pn"]:
            akinator = session.get('akinator')
            if not akinator:
                return jsonify({"error": "No game in progress"}), 400
            
            akinator.post_answer(answer)
            if akinator.answer_id:
                return jsonify({
                    "name": akinator.name,
                    "description": akinator.description
                }), 200
            else:
                return jsonify({"question": akinator.question}), 200
        else:
            return jsonify({"error": "Invalid answer"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/back', methods=['POST'])
def go_back():
    try:
        akinator = session.get('akinator')
        if not akinator:
            return jsonify({"error": "No game in progress"}), 400

        akinator.go_back()
        return jsonify({"question": akinator.question}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/exclude', methods=['POST'])
def exclude():
    try:
        akinator = session.get('akinator')
        if not akinator:
            return jsonify({"error": "No game in progress"}), 400

        akinator.exclude()
        return jsonify({"question": akinator.question}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/progress', methods=['GET'])
def progress():
    try:
        akinator = session.get('akinator')
        if not akinator:
            return jsonify({"error": "No game in progress"}), 400

        progression = akinator.progression
        step = akinator.step
        return jsonify({"progression": progression, "step": step}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
