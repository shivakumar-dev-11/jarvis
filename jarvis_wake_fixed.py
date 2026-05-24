import sounddevice as sd
from scipy.io.wavfile import write
import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import time

from rapidfuzz import fuzz

# ---------------- VOICE ENGINE ----------------
engine = pyttsx3.init()
engine.setProperty('rate', 170)

# ---------------- SPEAK ----------------
def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

# ---------------- LISTEN ----------------
def listen():

    fs = 44100
    seconds = 4

    print("Listening...")

    try:

        recording = sd.rec(
            int(seconds * fs),
            samplerate=fs,
            channels=1,
            dtype='int16'
        )

        sd.wait()

        write("audio.wav", fs, recording)

        r = sr.Recognizer()

        with sr.AudioFile("audio.wav") as source:
            audio = r.record(source)

        text = r.recognize_google(audio)

        text = text.lower().strip()

        print("You:", text)

        return text

    except:
        return ""

# ---------------- FUZZY MATCH ----------------
def match(command, keywords, threshold=90):

    for word in keywords:

        score = fuzz.partial_ratio(command, word)

        if score > threshold:
            return True

    return False

# ---------------- PROCESS COMMAND ----------------
def process(command):

    command = command.lower().strip()

    if command == "":
        return True

    print("Heard Command:", command)

    # ---------------- TIME ----------------
    if match(command, ["time", "tell time", "what is the time"]):

        now = datetime.datetime.now().strftime("%I:%M %p")

        speak(f"The time is {now}")

    # ---------------- DATE ----------------
    elif match(command, ["date", "today date"]):

        today = datetime.datetime.now().strftime("%d %B %Y")

        speak(f"Today's date is {today}")

    # ---------------- OPEN YOUTUBE ----------------
    elif match(command, ["open youtube", "youtube", "open you tube"]):

        speak("Opening YouTube")

        webbrowser.open("https://www.youtube.com")

    # ---------------- PLAY YOUTUBE ----------------
    elif match(command, ["play", "youtube play"]):

        query = (
            command
            .replace("play", "")
            .replace("youtube", "")
            .strip()
        )

        if query != "":

            speak(f"Playing {query} on YouTube")

            webbrowser.open(
                f"https://www.youtube.com/results?search_query={query}"
            )

        else:
            speak("What should I play?")

    # ---------------- GOOGLE SEARCH ----------------
    elif match(command, ["search", "google"]):

        query = (
            command
            .replace("search", "")
            .replace("google", "")
            .strip()
        )

        if query != "":

            speak(f"Searching Google for {query}")

            webbrowser.open(
                f"https://www.google.com/search?q={query}"
            )

        else:
            speak("What should I search?")

    # ---------------- OPEN GOOGLE ----------------
    elif match(command, ["open google"]):

        speak("Opening Google")

        webbrowser.open("https://www.google.com")

    # ---------------- GITHUB ----------------
    elif match(command, ["open github", "github", "git hub"]):

        speak("Opening GitHub")

        webbrowser.open("https://github.com")

    # ---------------- CHATGPT ----------------
    elif match(command, ["open chatgpt", "chatgpt"]):

        speak("Opening ChatGPT")

        webbrowser.open("https://chat.openai.com")

    # ---------------- SPOTIFY ----------------
    elif match(command, ["open spotify", "spotify"]):

        speak("Opening Spotify")

        webbrowser.open("https://open.spotify.com")

    # ---------------- INSTAGRAM ----------------
    elif match(command, ["open instagram", "instagram"]):

        speak("Opening Instagram")

        webbrowser.open("https://instagram.com")

    # ---------------- WHATSAPP ----------------
    elif match(command, ["open whatsapp", "whatsapp"]):

        speak("Opening WhatsApp")

        webbrowser.open("https://web.whatsapp.com")

    # ---------------- JOKE ----------------
    elif match(command, ["joke", "tell joke"]):

        speak(
            "Why do programmers hate bugs? Because they take forever to debug."
        )

    # ---------------- HOW ARE YOU ----------------
    elif match(command, ["how are you"]):

        speak("I am fine and ready to help you.")

    # ---------------- NAME ----------------
    elif match(command, ["your name", "who are you"]):

        speak("I am Jarvis, your personal assistant.")

    # ---------------- EXIT ----------------
    elif match(command, [
        "stop",
        "exit",
        "shutdown",
        "shut down",
        "close jarvis"
    ]):

        speak("Shutting down Jarvis")

        return False

    # ---------------- UNKNOWN ----------------
    else:

        speak(f"I heard {command}, but I don't know that yet.")

    return True

# ---------------- MAIN LOOP ----------------
def run():

    speak("Jarvis online. Say Jarvis to activate")

    while True:

        text = listen()

        if text == "":
            continue

        print("Heard:", text)

        # ---------------- WAKE WORD ----------------
        if match(text, ["jarvis"], 90):

            speak("Listening")

            command = listen()

            if command != "":

                if not process(command):
                    break

        time.sleep(0.3)

# ---------------- START ----------------
run()