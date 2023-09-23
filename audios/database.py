import speech_recognition as sr
from translate import Translator
import pymongo
from pymongo import MongoClient

# Initialize the MongoDB client
client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB connection string
db = client['your_database_name']
text_collection = db['Text']  # Create a new collection for text

def recognize_speech():
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Capture audio from the microphone
    with sr.Microphone() as source:
        print("Say something:")
        audio = recognizer.listen(source)

    # Recognize speech
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand what you said.")
        return None
    except sr.RequestError as e:
        print(f"Sorry, there was an error with the request: {e}")
        return None

def translate_and_store(input_text, language_code):
    # Translate the input text
    translator = Translator(to_lang=language_code)
    translated_text = translator.translate(input_text)

    # Store the translated text in MongoDB
    text_collection.insert_one({'language_code': language_code, 'translated_text': translated_text})

    return translated_text

if __name__ == "__main__":
    input_text = recognize_speech()
    
    if input_text:
        # Define the list of language codes for translation
        languages = ['en', 'ta', 'te', 'kn', 'ml', 'hi']

        # Translate and store the text for each language
        for lang_code in languages:
            translated_text = translate_and_store(input_text, lang_code)
            print(f"Translated text ({lang_code}): {translated_text}")
