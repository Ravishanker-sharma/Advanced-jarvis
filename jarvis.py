import time
import asyncio
import speech_recognition as sr
from chatbot import build_app, jarvis
import AppKit
from tools import show_popup

app = asyncio.run(build_app())

recognizer = sr.Recognizer()
recognizer.energy_threshold = 25

WAKE_WORD = "jarvis"
ACTIVE_WINDOW = 5  # seconds to stay active after wake word 
is_listening = True

def say_text(text, voice="com.apple.voice.compact.en-IN.Rishi", rate=175, volume=1.0):
    synth = AppKit.NSSpeechSynthesizer.alloc().init()
    if voice:
        synth.setVoice_(voice)
    synth.setRate_(rate)
    synth.setVolume_(volume)
    synth.startSpeakingString_(text)
    while synth.isSpeaking():
        time.sleep(0.1)

def listen():
    global is_listening
    active_until = 0  # timestamp until which assistant stays active

    while is_listening:
        with sr.Microphone() as source:
            print("🎤 Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                text = recognizer.recognize_google(audio).lower()
                print(text)

                current_time = time.time()
                # Check if wake word is detected or we are within active window
                if WAKE_WORD in text or current_time < active_until:
                    print("Working!")
                    output = asyncio.run(jarvis(app, text))
                    show_popup("Jarvis", output)
                    say_text(output)
                    # Extend the active window
                    active_until = time.time() + ACTIVE_WINDOW

            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                print("⚠️ Speech recognition service unavailable.")
            except Exception as e:
                print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    listen()
