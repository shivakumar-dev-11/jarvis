import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import speech_recognition as sr

fs = 44100
seconds = 5

print("Recording... speak now")

# IMPORTANT FIX: force int16 PCM format
recording = sd.rec(
    int(seconds * fs),
    samplerate=fs,
    channels=1,
    dtype='int16'
)

sd.wait()

# Save proper WAV file
write("audio.wav", fs, recording)

print("Processing speech...")

r = sr.Recognizer()

with sr.AudioFile("audio.wav") as source:
    audio = r.record(source)

try:
    text = r.recognize_google(audio)
    print("You said:", text)
except Exception as e:
    print("Error:", e)