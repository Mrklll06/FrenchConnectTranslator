from flask import Flask, render_template, request
from gtts import gTTS
from deep_translator import GoogleTranslator
import os

app = Flask(__name__)

# Home Page
@app.route("/", methods=["GET", "POST"])
def home():
    translated_text = ""
    audio_file = None

    if request.method == "POST":
        text = request.form["text"]
        lang = request.form["lang"]

        if lang == "en_to_fr":
            translated_text = GoogleTranslator(source="en", target="fr").translate(text)
        elif lang == "fr_to_en":
            translated_text = GoogleTranslator(source="fr", target="en").translate(text)

        # Generate audio file if requested
        if "audio" in request.form:
            tts = gTTS(text=translated_text, lang="fr" if lang == "en_to_fr" else "en")
            audio_file = "static/audio.mp3"
            tts.save(audio_file)

    return render_template("index.html", translated_text=translated_text, audio_file=audio_file)

if __name__ == "__main__":
    app.run(debug=True)
