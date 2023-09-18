import speech_recognition as sr
from translate import Translator
from gtts import gTTS
import pygame

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

def translate_and_save(input_text):
    # Define language codes for the supported languages
    language_codes = {
        'en': 'English',
        'ta': 'Tamil',
        'te': 'Telugu',
        'kn': 'Kannada',
        'ml': 'Malayalam',
    }

    # Create a folder to save text and audio files (if it doesn't exist)
    import os
    if not os.path.exists("translations"):
        os.makedirs("translations")

    output_text_file = "translations/translated_texts.txt"

    with open(output_text_file, "w", encoding="utf-8") as text_file:
        pygame.init()

        for lang_code, lang_name in language_codes.items():
            translator = Translator(to_lang=lang_code)
            translated_text = translator.translate(input_text)

            # Create a gTTS object for the translated text
            tts = gTTS(text=translated_text, lang=lang_code)

            # Save the speech as an audio file with language code in the filename
            audio_file_name = f"translations/{lang_code}_translated_audio.mp3"
            tts.save(audio_file_name)

            print(f"Saved {lang_name} audio as {audio_file_name}")

            # Display translated text in the terminal with a header
            print(f"--- {lang_name} Translation ---")
            print(translated_text)
            print()

            # Write translated text to the text file with headers and spaces
            text_file.write(f"--- {lang_name} Translation ---\n")
            text_file.write(translated_text + "\n\n")

            # Play the corresponding audio
            pygame.mixer.init()
            pygame.mixer.music.load(audio_file_name)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.delay(100)

        print(f"Translations saved to {output_text_file}")

if __name__ == "__main__":
    input_text = recognize_speech()
    
    if input_text:
        translate_and_save(input_text)
