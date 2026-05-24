import speech_recognition as sr

r = sr.Recognizer()

print("Testing microphone... speak now")

with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)
    audio = r.listen(source)

try:
    text = r.recognize_google(audio)
    print("You said:", text)
except:
    print("Could not understand audio")