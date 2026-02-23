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
        if fuzz.ratio(word, WAKE_WORD) > 60:
            return True
    return False

def open_google_search(query):
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.google.com/search?q={encoded_query}"
    webbrowser.open(url)

def start_voice(ui):
    recognizer = sr.Recognizer()

    # 🔥 Improve recognition accuracy
    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 1.5
    recognizer.phrase_threshold = 0.3
    recognizer.non_speaking_duration = 0.8

    mic = sr.Microphone()
    active_mode = False

    with mic as source:
        print("Calibrating microphone...")
        recognizer.adjust_for_ambient_noise(source, duration=1)

    ui.speak("Rooney system ready.")

    while True:
        try:
            # 🚫 Prevent assistant from hearing itself
            if ui.is_speaking:
                time.sleep(0.3)
                continue

            with mic as source:
                print("Listening...")
                audio = recognizer.listen(source, timeout=None)

            try:
                command = recognizer.recognize_google(audio, language="en-US").lower()
                print("You said:", command)
            except:
                continue

            # 🟢 Wake Word Detection
            if not active_mode and wake_detected(command):
                active_mode = True
                ui.listening = True
                ui.status_label.setText("Active Mode")
                ui.speak("I'm here.")
                continue

            if active_mode:

                # 🔵 Sleep Mode
                if any(phrase in command for phrase in SLEEP_WORDS):
                    active_mode = False
                    ui.listening = False
                    ui.status_label.setText("Waiting for wake word...")
                    ui.speak("Going to sleep.")
                    continue

                # 🔎 Google Search With Confirmation
                if command.startswith("search"):
                    query = command.replace("search", "").strip()

                    if query:
                        ui.speak(f"Did you say search for {query}?")

                        # Listen for confirmation
                        with mic as source:
                            print("Confirming...")
                            confirm_audio = recognizer.listen(source)

                        try:
                            confirmation = recognizer.recognize_google(confirm_audio, language="en-US").lower()
                            print("Confirmation:", confirmation)

                            if "yes" in confirmation:
                                ui.speak(f"Searching Google for {query}")
                                open_google_search(query)
                            else:
                                ui.speak("Search cancelled.")
                        except:
                            ui.speak("I didn't catch that. Cancelling search.")

                    continue

                # 🌐 Open Google directly
                if command.startswith("open google"):
                    ui.speak("Opening Google")
                    webbrowser.open("https://www.google.com")
                    continue

                # 🤖 Normal AI Response
                response = ask_rooney(command)

                if response:
                    ui.speak(response)

        except Exception as e:
            print("Error:", e)
            continue