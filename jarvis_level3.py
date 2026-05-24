import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
import pyttsx3
from google import genai
import os

# =========================
# TEXT TO SPEECH ENGINE
# =========================
engine = pyttsx3.init()
engine.setProperty('rate', 180)

def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

# =========================
# GEMINI AI SETUP (FIXED)
# =========================
client = genai.Client(api_key="")

def ask_ai(prompt):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"AI Error: {e}"

# =========================
# VOICE INPUT (NO PY AUDIO)
# =========================
def listen():
    fs = 16000
    duration = 5

    print("Listening...")

    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()

    wav.write("input.wav", fs, recording)

    recognizer = sr.Recognizer()

    with sr.AudioFile("input.wav") as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio)
        print("Heard:", text)
        return text.lower()
    except:
        return ""

# =========================
# MAIN LOGIC
# =========================
def process_command(command):
    if not command:
        return

    if "exit" in command or "stop" in command:
        speak("Goodbye!")
        exit()

    if "hello" in command or "hi" in command:
        speak("Hello! I am Jarvis Level 3.")
        return

    # AI RESPONSE
    speak("Thinking...")
    reply = ask_ai(command)
    speak(reply)

# =========================
# MAIN LOOP
# =========================
def run():
    speak("Jarvis Level 3 Stable Running")

    while True:
        command = listen()
        print("Command:", command)
        process_command(command)

if __name__ == "__main__":
    run()