import re
import random
import speech_recognition as sr
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

chatbot = pipeline("conversational")

faq_responses = {}
with open("static/faq_responses.txt", "r") as faq_file:
    lines = faq_file.readlines()
    for line in lines:
        q, a = line.strip().split("#")
        faq_responses[q] = a

sentence_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Facebook Messenger and Instagram integration
facebook_messenger_access_token = "EAAJb4qObFZA4BOyFiRj7G6XDKBgE2C1UlHlHIYmYM4Pmyi0sL7A7RRDJIUrWkXGe94gbZBX4pCXJQ0ZBwTOhZAFFNbS6H9k33Hw1cSMVWelZBD2NPs5EYZCZAX6DVvGT6eDotOAZCtRUYuzKLSKDh9ZA1lGpngEGvZCiT5lhLLOL11fZBNoLoMRZCDFWnezYV2Lqtw0959re6yTq"
facebook_messenger_page_id = "122449060955941"
instagram_business_account_id = "sid_art272"

# Create a session for sending requests to Facebook API
facebook_session = requests.Session()
facebook_session.headers.update({"Content-Type": "application/json"})
facebook_session.params = {"access_token": facebook_messenger_access_token}

# Initialize the speech recognizer
recognizer = sr.Recognizer()

def text_chatbot(user_input):
    response = chatbot(user_input)[0]['generated_text']
    return response

def semantic_search(query, faq_responses, threshold=0.7):
    query_embedding = sentence_model.encode([query], convert_to_tensor=True)
    faq_embeddings = sentence_model.encode(list(faq_responses.keys()), convert_to_tensor=True)
    cos_scores = util.pytorch_cos_sim(query_embedding, faq_embeddings)[0]
    similar_questions = []
    for i, score in enumerate(cos_scores):
        if score > threshold:
            similar_questions.append(list(faq_responses.keys())[i])  
    return similar_questions

def speech_recognition():
    with sr.Microphone() as source:
        print("Listening... (Say 'exit' to quit)")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        user_input = recognizer.recognize_google(audio).lower()
        print("You said:", user_input)
        return user_input
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand.")
        return ""
    except sr.RequestError:
        print("Sorry, I encountered an error while trying to access the Google API.")
        return ""

def send_facebook_messenger_message(user_id, message):
    data = {
        "recipient": {"id": user_id},
        "message": {"text": message}
    }
    response = facebook_session.post(
        f"https://graph.facebook.com/v14.0/{facebook_messenger_page_id}/messages",
        json=data
    )
    if response.status_code != 200:
        print("Failed to send message to Facebook Messenger:", response.text)

def send_instagram_message(user_id, message):
    data = {
        "recipient": {"id": user_id},
        "message": {"text": message}
    }
    response = facebook_session.post(
        f"https://graph.facebook.com/v14.0/me/messages/?business_id={instagram_business_account_id}",
        json=data
    )
    if response.status_code != 200:
        print("Failed to send message to Instagram:", response.text)

def get_response(user_input):
    user_input = user_input.strip().lower()
    if user_input == "exit":
        print("Goodbye!")
        return "Goodbye!"
    similar_questions = semantic_search(user_input, faq_responses)
    if similar_questions:
        response = faq_responses[similar_questions[0]]
        return response
    return "I'm sorry, I don't have an answer for that."

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_bot_response():
    user_input = request.form["user_input"]
    response = get_response(user_input)

    # Send the response to Facebook Messenger and Instagram
    user_id = request.args.get("user_id")
    send_facebook_messenger_message(user_id, response)
    send_instagram_message(user_id, response)

    return jsonify({"response": response})

@app.route("/process_audio", methods=["POST"])
def process_audio():
    try:
        audio = request.files['audio']
        audio.save("user_audio.wav")
        with sr.AudioFile("user_audio.wav") as source:
            audio_data = recognizer.record(source)
            try:
                transcribed_text = recognizer.recognize_google(audio_data)
                return transcribed_text
            except sr.UnknownValueError:
                return "Sorry, I couldn't understand the recording."
    except Exception as e:
        print("Error processing audio:", e)
        return "An error occurred while processing the audio."

if __name__ == "__main__":
    recognizer=sr.Recognizer()
    app.run(debug=True)
