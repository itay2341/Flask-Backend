from flask import Flask, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI
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
    
    try:
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ],
            max_tokens=40
        )
        answer = response.choices[0].message.content.strip()

        return jsonify({'question': question, 'answer': answer}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
