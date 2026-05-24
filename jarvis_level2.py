import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import json
import google.generativeai as genai

# ===================== CONFIG =====================

API_KEY = ""

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash-latest")

engine = pyttsx3.init()
engine.setProperty("rate", 170)

MEMORY_FILE = "memory.json"

# ===================== MEMORY =====================

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {}

def save_memory(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f)

memory = load_memory()

# ===================== SPEAK =====================

def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

# ===================== LISTEN =====================

def listen():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print("Heard:", text)
        return text.lower()
    except:
        return ""

# ===================== AI =====================

def ask_ai(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print("AI Error:", e)
        return "I couldn't process that right now."

# ===================== MAC APP CONTROL =====================

def open_app(app_name):
    apps = {
        "chrome": "Google Chrome",
        "safari": "Safari",
        "notes": "Notes",
        "calculator": "Calculator",
        "terminal": "Terminal",
        "spotify": "Spotify",
        "finder": "Finder"
    }

    if app_name in apps:
        os.system(f"open -a '{apps[app_name]}'")
        speak(f"Opening {app_name}")
    else:
        speak("App not found")

# ===================== COMMAND HANDLER =====================

def handle_command(command):

    # -------- NAME MEMORY --------
    if "my name is" in command:
        name = command.replace("my name is", "").strip()
        memory["name"] = name
        save_memory(memory)
        speak(f"Okay {name}, I will remember that.")
        return

    if "what is my name" in command:
        name = memory.get("name", None)
        if name:
            speak(f"Your name is {name}")
        else:
            speak("I don't know your name yet")
        return

    # -------- TIME --------
    if "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}")
        return

    # -------- WEB --------
    if "open google" in command:
        webbrowser.open("https://google.com")
        speak("Opening Google")
        return

    if "open youtube" in command:
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube")
        return

    # -------- APPS --------
    if "open" in command:
        for app in ["chrome", "safari", "notes", "calculator", "terminal", "spotify", "finder"]:
            if app in command:
                open_app(app)
                return

    # -------- EXIT --------
    if "exit" in command or "stop" in command:
        speak("Shutting down")
        exit()

    # -------- AI FALLBACK --------
    reply = ask_ai(command)
    speak(reply)

# ===================== WAKE WORD SYSTEM =====================

def run():
    speak("Jarvis Level 2 online. Say 'jarvis' to activate")

    while True:
        text = listen()

        if "jarvis" in text:
            speak("Yes?")
            command = listen()

            if command:
                print("Command:", command)
                handle_command(command)

# ===================== START =====================

run()