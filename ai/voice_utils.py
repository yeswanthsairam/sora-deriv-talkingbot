import tempfile
import sounddevice as sd
import wavio
import speech_recognition as sr
import pyttsx3

recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

def record_audio(seconds=5, samplerate=44100):
    """Record audio from microphone."""
    audio = sd.rec(int(seconds * samplerate), samplerate=samplerate, channels=1, dtype="int16")
    sd.wait()
    return audio, samplerate

def save_audio(audio, samplerate):
    """Save audio to temporary file and return path."""
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    wavio.write(temp_file.name, audio, samplerate, sampwidth=2)
    return temp_file.name

def speech_to_text(file_path):
    """Convert speech (wav file) to text."""
    with sr.AudioFile(file_path) as source:
        audio_data = recognizer.record(source)
        return recognizer.recognize_google(audio_data)

def text_to_speech(text):
    """Convert text to spoken audio."""
    tts_engine.say(text)
    tts_engine.runAndWait()
