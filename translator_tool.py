from tkinter import Tk, Label, Text, END, filedialog
from tkinter.ttk import Button
from threading import Timer
from deep_translator import GoogleTranslator
from gtts import gTTS
import pygame

# Initialize pygame mixer
pygame.mixer.init()

# Global Timer variables
english_timer = None
french_timer = None

# Functions for delayed translation
def delayed_translate_to_french():
    input_text = english_text.get("1.0", END).strip()
    if input_text:
        translated_text = GoogleTranslator(source='en', target='fr').translate(input_text)
        french_text.delete("1.0", END)
        french_text.insert(END, translated_text)
    else:
        french_text.delete("1.0", END)

def delayed_translate_to_english():
    input_text = french_text.get("1.0", END).strip()
    if input_text:
        translated_text = GoogleTranslator(source='fr', target='en').translate(input_text)
        english_text.delete("1.0", END)
        english_text.insert(END, translated_text)
    else:
        english_text.delete("1.0", END)

def schedule_translation_to_french(event=None):
    global english_timer
    if english_timer is not None:
        english_timer.cancel()
    english_timer = Timer(0.5, delayed_translate_to_french)  # 500ms delay
    english_timer.start()

def schedule_translation_to_english(event=None):
    global french_timer
    if french_timer is not None:
        french_timer.cancel()
    french_timer = Timer(0.5, delayed_translate_to_english)  # 500ms delay
    french_timer.start()

def save_translation():
    english_content = english_text.get("1.0", END).strip()
    french_content = french_text.get("1.0", END).strip()
    if english_content or french_content:
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt"),
                                                            ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write("Translation Saved by French Connect Translator Tool\n")
                    file.write("---------------------------------------------------\n\n")
                    file.write("English Text:\n")
                    file.write(english_content + "\n\n")
                    file.write("French Text:\n")
                    file.write(french_content + "\n")
                status_label.config(text="Translation saved successfully!")
            except Exception as e:
                status_label.config(text=f"Error saving file: {e}")
    else:
        status_label.config(text="Nothing to save!")

def play_english_audio():
    text = english_text.get("1.0", END).strip()
    if text:
        try:
            temp_audio_path = "english_audio.mp3"  # Create a temp file
            tts = gTTS(text=text, lang='en')
            tts.save(temp_audio_path)
            pygame.mixer.music.load(temp_audio_path)  # Load the audio
            pygame.mixer.music.play()  # Play the audio
        except Exception as e:
            status_label.config(text=f"Error playing audio: {e}")

def play_french_audio():
    text = french_text.get("1.0", END).strip()
    if text:
        try:
            temp_audio_path = "french_audio.mp3"  # Create a temp file
            tts = gTTS(text=text, lang='fr')
            tts.save(temp_audio_path)
            pygame.mixer.music.load(temp_audio_path)  # Load the audio
            pygame.mixer.music.play()  # Play the audio
        except Exception as e:
            status_label.config(text=f"Error playing audio: {e}")

def save_english_audio():
    text = english_text.get("1.0", END).strip()
    if text:
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".mp3",
                                                     filetypes=[("MP3 files", "*.mp3"),
                                                                ("All files", "*.*")])
            if file_path:
                tts = gTTS(text=text, lang='en')
                tts.save(file_path)
                status_label.config(text="English audio saved successfully!")
        except Exception as e:
            status_label.config(text=f"Error saving audio: {e}")

def save_french_audio():
    text = french_text.get("1.0", END).strip()
    if text:
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".mp3",
                                                     filetypes=[("MP3 files", "*.mp3"),
                                                                ("All files", "*.*")])
            if file_path:
                tts = gTTS(text=text, lang='fr')
                tts.save(file_path)
                status_label.config(text="French audio saved successfully!")
        except Exception as e:
            status_label.config(text=f"Error saving audio: {e}")

# GUI Setup
root = Tk()
root.title("French Connect Translator Tool")
root.geometry("800x800")

# English Input Box
Label(root, text="English", font=("Arial", 14)).pack(pady=5)
english_text = Text(root, height=10, width=70)
english_text.pack(pady=5)
english_text.bind("<KeyRelease>", schedule_translation_to_french)  # Delayed translation on typing

Button(root, text="Play English Audio", command=play_english_audio).pack(pady=5)
Button(root, text="Save English Audio", command=save_english_audio).pack(pady=5)

# French Input Box
Label(root, text="French", font=("Arial", 14)).pack(pady=5)
french_text = Text(root, height=10, width=70)
french_text.pack(pady=5)
french_text.bind("<KeyRelease>", schedule_translation_to_english)  # Delayed translation on typing

Button(root, text="Play French Audio", command=play_french_audio).pack(pady=5)
Button(root, text="Save French Audio", command=save_french_audio).pack(pady=5)

# Save Button
Button(root, text="Save Translation", command=save_translation).pack(pady=10)

# Status Label
status_label = Label(root, text="", font=("Arial", 10))
status_label.pack(pady=5)

# Run the GUI
root.mainloop()
