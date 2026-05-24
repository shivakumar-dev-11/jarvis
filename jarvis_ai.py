import sounddevice as sd
from scipy.io.wavfile import write
import speech_recognition as sr
import google.generativeai as genai
import pyttsx3
import datetime
import webbrowser
import os

# =========================
# 🔑 GEMINI API KEY
# =========================
genai.configure(api_key="")

model = genai.GenerativeModel("gemini-1.5-flash-latest")

# =========================
# 🔊 VOICE ENGINE
# =========================
engine = pyttsx3.init()

def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

# =========================
# 🤖 GEMINI RESPONSE
# =========================
def ask_ai(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI Error: {e}"

# =========================
# 🎤 VOICE INPUT (NO PY AUDIO)
# =========================
def listen():
    fs = 44100
    seconds = 4

    print("Listening...")

    recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()

    write("audio.wav", fs, recording)

    r = sr.Recognizer()

    try:
        with sr.AudioFile("audio.wav") as source:
            audio = r.record(source)

        text = r.recognize_google(audio)
        print("Heard:", text)
        return text.lower()

    except:
        return ""

# =========================
# 🧠 COMMAND ENGINE
# =========================
def process_command(command):

    # TIME
    if "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}")
        return

    # CHROME
    if "open chrome" in command or "chrome" in command:
        speak("Opening Chrome")
        os.system("open -a Google\\ Chrome")
        return

    # YOUTUBE
    if "youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")
        return

    # GOOGLE
    if "google" in command:
        speak("Opening Google")
        webbrowser.open("https://google.com")
        return

    # EXIT
    if "exit" in command or "stop" in command:
        speak("Shutting down Jarvis")
        exit()

    # 🤖 AI FALLBACK
    reply = ask_ai(command)
    speak(reply)

# =========================
# 🚀 MAIN LOOP
# =========================
def run():
    speak("Jarvis AI online")

    while True:
        command = listen()

        if command == "":
            continue

        print("Heard Command:", command)

        process_command(command)

# =========================
# START
# =========================
run()