import sounddevice as sd
import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import queue

# ---------------- VOICE ----------------
engine = pyttsx3.init()
engine.setProperty('rate', 170)

def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

# ---------------- AUDIO QUEUE ----------------
audio_queue = queue.Queue()

def callback(indata, frames, time, status):
    audio_queue.put(bytes(indata))

# ---------------- LISTEN FUNCTION ----------------
def listen_command():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening for command...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio).lower()
        print("You:", text)
        return text
    except:
        return ""

# ---------------- COMMANDS ----------------
def process(cmd):

    if "time" in cmd:
        speak(datetime.datetime.now().strftime("%I:%M %p"))

    elif "open chrome" in cmd:
        speak("Opening Chrome")
        webbrowser.open("https://google.com")

    elif "search google for" in cmd:
        q = cmd.replace("search google for", "")
        webbrowser.open(f"https://google.com/search?q={q}")
        speak(f"Searching {q}")

    elif "play youtube" in cmd:
        q = cmd.replace("play youtube", "")
        webbrowser.open(f"https://youtube.com/results?search_query={q}")
        speak(f"Playing {q}")

    elif "stop" in cmd or "exit" in cmd:
        speak("Shutting down")
        return False

    else:
        speak("I didn't understand that")

    return True

# ---------------- WAKE WORD LOOP ----------------
def run():
    speak("Jarvis online. Say 'Jarvis' to activate")

    while True:
        text = listen_command()

        # WAKE WORD TRIGGER
        if "jarvis" in text:
            speak("Yes?")
            cmd = listen_command()
            if not process(cmd):
                break

# ---------------- START ----------------
run()