from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import google.generativeai as genai
import os

app = Flask(__name__)

# Gemini API setup
genai.configure(api_key=os.environ.get("AIzaSyDcO5zCyu-afbdmLvVRkoCiBb0c36tUZlE"))
model = genai.GenerativeModel('gemini-pro')

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# API to handle audio to Gemini response
@app.route('/ask', methods=['POST'])
def ask():
    recognizer = sr.Recognizer()
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file'}), 400

    audio_file = request.files['audio']

    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
            print("Recognized:", text)
        except Exception as e:
            return jsonify({'error': f"Speech Recognition failed: {str(e)}"}), 500

    # Ask Gemini
    try:
        response = model.generate_content(text)
        return jsonify({'question': text, 'response': response.text})
    except Exception as e:
        return jsonify({'error': f"Gemini error: {str(e)}"}), 500

# Run with proper host/port for Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Default to 10000 if not set
    app.run(host='0.0.0.0', port=port)
