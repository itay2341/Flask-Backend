from flask import Flask, request, jsonify
from dotenv import load_dotenv
from models import db, Message
from openai import OpenAI
import os

load_dotenv('.env.docker' if os.getenv('FLASK_ENV') == 'docker' else '.env.local')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route('/ask', methods=['POST'])
def ask_question():
    if not request.json or 'question' not in request.json:
        return jsonify({'error': 'Invalid request'}), 400
    
    question = request.json['question']
    
    try:
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        chat_history = Message.get_all_messages_sorted_by_created_time()
        chat_history.append({"role": "user", "content": question})

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=chat_history
        )
        answer = response.choices[0].message.content.strip()

        Message(role="user", content=question).save()
        Message(role="assistant", content=answer).save()

        return jsonify({'question': question, 'answer': answer}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
