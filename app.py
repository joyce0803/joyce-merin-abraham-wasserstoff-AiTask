from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import json
import os
from dotenv import load_dotenv
import google.generativeai as genai
from text_preprocessing import preprocess_text
from generate_embeddings import process_documents, get_vector_store
from reAct_and_rag import create_retriever
from reAct_and_rag import generate_response
from langchain_community.chat_message_histories import ChatMessageHistory
from reAct_and_rag import suggestions
from flask import session
import uuid



app = Flask(__name__)
app.secret_key = '192b9bdd22ab9ed4d12e236c78afc'
CORS(app)
load_dotenv()

api_key = os.getenv('GOOGLE_API_KEY')
api_key = os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=api_key)

# cache dictionary
cache = {}

#chat history
store = {}

# Cache expiration time in seconds
CACHE_EXPIRATION = 300  # 5 minutes

session_id = None
TEXT_DATA_DIR = 'text_data'
os.makedirs(TEXT_DATA_DIR, exist_ok=True)

def generate_session_id():
    return str(uuid.uuid4())


def get_session_history(session_id: str) -> ChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# def create_vector():
#     file_path = os.path.join(TEXT_DATA_DIR, "data.txt")
#     if os.path.exists(file_path):
#         with open(file_path, 'r', encoding='utf-8') as file:
#             data = file.read()
#
#     print(data)


def save_json_data(data, filename):
    """Save JSON data to a file."""
    file_path = os.path.join(TEXT_DATA_DIR, filename)
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)  # Serialize data to a JSON formatted string and write it to file
    return file_path
    
def load_json_data(filename):
    """Load JSON data from a file."""
    file_path = os.path.join(TEXT_DATA_DIR, filename)
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)  # Deserialize the JSON data back into a dictionary
    return None


@app.route("/")
def index():
    session_id = session.get('session_id', generate_session_id())
    session['session_id'] = session_id  # Save or refresh the session ID in the user's session
    return render_template('chat.html', session_id=session_id)


@app.route("/load_data", methods=["POST"])
def load_data():
    data = request.get_json()
    cache_key = 'posts_pages_data'
    current_time = datetime.now().timestamp()

    # Check if data is already in cache and not expired
    if cache_key in cache and (current_time - cache[cache_key]['timestamp']) < CACHE_EXPIRATION:
        print("Returning cached data")
        return jsonify({"status": "Data returned from cache", "data": cache[cache_key]['data']})

    if data:
        print(data)
        # Preprocess each post and page content
        data['posts'] = [preprocess_text(post) for post in data['posts']]
        data['pages'] = [preprocess_text(page) for page in data['pages']]
        cache[cache_key] = {
            'data': data,
            'timestamp': current_time
        }
        print("Data processed and cached")
        print(data)
        file_path = save_json_data(data, "data.json")
        return jsonify({"status": "Data saved successfully", "file_path": file_path})
    else:
        return jsonify({"status": "No data received"}), 400


@app.route("/get", methods=["GET", "POST"])
def chat():

    msg = request.form["msg"]
    user_input = msg
    data = load_json_data("data.json")
    if data:
        text_chunks = process_documents(data)
        vector_store = get_vector_store(text_chunks)  # creating vector store
        tools = create_retriever(vector_store)

        answer = generate_response(tools, user_input, session_id)
        suggest = suggestions(user_input)
        print(suggest)
        return jsonify({"message": answer, "suggestions": suggest})



if __name__ == '__main__':
    app.run(debug=True)