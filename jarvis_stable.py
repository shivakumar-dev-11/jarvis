import sounddevice as sd
from scipy.io.wavfile import write
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import google.generativeai as genai

# ================= CONFIG =================

API_KEY = ""

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash-latest")

engine = pyttsx3.init()
engine.setProperty("rate", 170)

# ================= SPEAK =================

def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

# ================= LISTEN (NO PYAUDIO) =================

def listen():
    fs = 44100
    seconds = 4

    print("Listening...")

    recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()

    write("audio.wav", fs, recording)

    r = sr.Recognizer()

    with sr.AudioFile("audio.wav") as source:
        audio = r.record(source)

    try:
        text = r.recognize_google(audio)
        print("Heard:", text)
        return text.lower()
    except:
        return ""

# ================= AI =================

def ask_ai(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print("AI Error:", e)
        return "Sorry, I couldn't process that."

# ================= COMMANDS =================

def handle_command(cmd):

    if "time" in cmd:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}")
        return

    elif "open google" in cmd:
        webbrowser.open("https://google.com")
        speak("Opening Google")
        return

    elif "open youtube" in cmd:
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube")
        return

    elif "open chrome" in cmd:
        os.system("open -a 'Google Chrome'")
        speak("Opening Chrome")
        return

    elif "open notes" in cmd:
        os.system("open -a 'Notes'")
        speak("Opening Notes")
        return

    elif "exit" in cmd or "stop" in cmd:
        speak("Shutting down Jarvis")
        exit()

    else:
        reply = ask_ai(cmd)
        speak(reply)

# ================= MAIN LOOP =================

def run():
    speak("Jarvis stable version online. Say Jarvis to activate")

    while True:
        text = listen()

        if "jarvis" in text:
            speak("Yes?")
            command = listen()

            if command:
                print("Command:", command)
                handle_command(command)

# ================= START =================

run()