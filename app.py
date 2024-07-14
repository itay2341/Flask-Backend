from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os


if os.getenv('FLASK_ENV') == 'docker':
    load_dotenv('.env.docker')
else:
    load_dotenv('.env.local')

app = Flask(__name__)


@app.route('/ask', methods=['POST'])
def ask_question():
    try:
        question = request.json['question']
    except:
        return jsonify({'error': 'Invalid request'}), 400
    
    return jsonify({'question': question, 'answer': 'answer'}), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
