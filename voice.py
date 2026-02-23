import speech_recognition as sr
from brain import ask_rooney
from rapidfuzz import fuzz
import webbrowser
import urllib.parse
import time

WAKE_WORD = "rooney"
SLEEP_WORDS = ["go to sleep", "stop listening", "goodnight"]

def wake_detected(text):
    words = text.split()
    for word in words:
        if fuzz.ratio(word, WAKE_WORD) > 55:
            return True
    return False

def open_google_search(query):
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.google.com/search?q={encoded_query}"
    webbrowser.open(url)

def start_voice(ui):
    recognizer = sr.Recognizer()

    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 2.0
    recognizer.non_speaking_duration = 1.0

    mic = sr.Microphone()
    active_mode = False

    with mic as source:
        print("Calibrating microphone...")
        recognizer.adjust_for_ambient_noise(source, duration=1)

    ui.speak("Rooney system ready.")

    while True:
        try:
            if ui.is_speaking:
                time.sleep(0.2)
                continue

            with mic as source:
                print("Listening...")
                audio = recognizer.listen(source)

            try:
                command = recognizer.recognize_google(audio).lower()
                print("You said:", command)
            except:
                continue

            # Wake word activation
            if not active_mode and wake_detected(command):
                active_mode = True
                ui.listening = True
                ui.status_label.setText("Active Mode")
                ui.speak("I'm here.")
                continue

            if active_mode:

                # Sleep mode
                if any(phrase in command for phrase in SLEEP_WORDS):
                    active_mode = False
                    ui.listening = False
                    ui.status_label.setText("Waiting for wake word...")
                    ui.speak("Going to sleep.")
                    continue

                # 🔥 GOOGLE SEARCH COMMAND
                if command.startswith("search"):
                    query = command.replace("search", "").strip()
                    if query:
                        ui.speak(f"Searching Google for {query}")
                        open_google_search(query)
                    continue

                if command.startswith("open google"):
                    ui.speak("Opening Google")
                    webbrowser.open("https://www.google.com")
                    continue

                # Default AI response
                response = ask_rooney(command)
                ui.speak(response)

        except Exception as e:
            print("Error:", e)
            continue