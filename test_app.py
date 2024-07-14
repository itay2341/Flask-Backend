from app import app
import pytest


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_ask_question(client):
    """
    Test that the chatbot can answer a question.
    """
    response = client.post('/ask', json={'question': 'What is the capital of France?'})
    assert response.status_code == 200, "The response should be a success"
    data = response.get_json()
    assert 'answer' in data and 'question' in data, "The response should contain an answer and a question"
    assert 'paris' in data['answer'].lower(), "The answer should be Paris"



def test_remember_conversation(client):
    """
    Test that the chatbot can remember the conversation.
    """
    # First question
    response = client.post('/ask', json={'question': 'What is the capital of Israel?'})
    assert response.status_code == 200, "The response should be a success"

    # Second question
    response = client.post('/ask', json={'question': 'What is AI?'})
    assert response.status_code == 200, "The response should be a success"

    # Ask the chatbot to remember the last question
    response = client.post('/ask', json={'question': 'What the last question I asked you? (please quote me)'})
    assert response.status_code == 200, "The response should be a success" 
    data = response.get_json()
    assert 'what is ai' in data['answer'].lower()

    response = client.post('/ask', json={'question': 'What did I ask you before that question? (please quote me)'})
    assert response.status_code == 200, "The response should be a success"
    data = response.get_json()
    assert 'what is the capital of israel' in data['answer'].lower()

