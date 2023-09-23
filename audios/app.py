# app.py
from flask import Flask, request, render_template, jsonify
from pymongo import MongoClient
from translate import Translator
from gtts import gTTS
import os

app = Flask(__name__)

# Initialize the MongoDB client
client = MongoClient('mongodb://localhost:27017/')
db = client['your_database_name']
text_collection = db['Text']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        language_code = request.form.get('language_code')
        
        # Retrieve the latest text from the database
        latest_text_doc = text_collection.find_one(sort=[('_id', -1)])
        latest_text = latest_text_doc['translated_text']
        
        # Translate the latest text to the selected language
        translator = Translator(to_lang=language_code)
        translated_text = translator.translate(latest_text)

        # Convert the translated text to audio
        tts = gTTS(text=translated_text, lang=language_code)
        audio_file_name = f"static/audio_{language_code}.mp3"
        tts.save(audio_file_name)

        return render_template('index.html', translated_text=translated_text, audio_file=audio_file_name)
    
    return render_template('index.html', translated_text='', audio_file='')

if __name__ == "__main__":
    app.run(debug=True)
