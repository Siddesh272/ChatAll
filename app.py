import flask
from flask import Flask, render_template, request, jsonify
import requests
import json
from modules.chatbot import text_chatbot, semantic_search, get_response
from modules.speech import speech_recognition
from modules.facebook import send_facebook_messenger_message, send_instagram_message
from flask_compress import Compress

app = Flask(__name__)
Compress(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_bot_response():
    user_input = request.form["user_input"]
    response = get_response(user_input)
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
    app.run(debug=True)
