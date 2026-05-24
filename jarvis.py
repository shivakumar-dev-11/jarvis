import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import time

# ---------------- VOICE ENGINE ----------------
engine = pyttsx3.init()
engine.setProperty('rate', 170)

def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

# ---------------- RECORD AUDIO ----------------
def record_audio(seconds=4, fs=44100):
    recording = sd.rec(
        int(seconds * fs),
        samplerate=fs,
        channels=1,
        dtype='int16'
    )
    sd.wait()
    write("audio.wav", fs, recording)

# ---------------- SPEECH TO TEXT ----------------
def listen():
    record_audio()

    r = sr.Recognizer()
    with sr.AudioFile("audio.wav") as source:
        audio = r.record(source)

    try:
        command = r.recognize_google(audio)
        print("You:", command)
        return command.lower()
    except:
        return ""

# ---------------- COMMAND ENGINE ----------------
def process(command):

    if "time" in command:
        time_now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {time_now}")

    elif "open chrome" in command:
        speak("Opening Chrome")
        webbrowser.open("https://google.com")

    elif "search google for" in command:
        query = command.replace("search google for", "")
        speak(f"Searching Google for {query}")
        webbrowser.open(f"https://www.google.com/search?q={query}")

    elif "play youtube" in command:
        query = command.replace("play youtube", "")
        speak(f"Playing {query} on YouTube")
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")

    elif "exit" in command or "stop" in command:
        speak("Shutting down")
        return False

    elif command != "":
        speak("I heard you but I don't know that command")

    return True

# ---------------- MAIN LOOP ----------------
def run():
    speak("Jarvis is now online")

    running = True
    while running:
        command = listen()
        running = process(command)
        time.sleep(1)

# ---------------- START ----------------
run()