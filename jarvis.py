from chatbot import chat
import speech_recognition as sr
# import pyttsx3
import time
import AppKit




recognizer = sr.Recognizer()
recognizer.energy_threshold = 25

is_listening = True

# engine = pyttsx3.init('sapi5')
# engine.setProperty('rate', 160)  # Adjusted speed
# voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[0].id)


def say_text(text, voice="com.apple.voice.compact.en-IN.Rishi", rate=175, volume=1.0):
    """Speak text using macOS TTS with optional voice, rate, and volume."""
    synth = AppKit.NSSpeechSynthesizer.alloc().init()
    
    if voice:
        synth.setVoice_(voice)
    synth.setRate_(rate)     # speaking rate (default ~175)
    synth.setVolume_(volume) # volume 0.0 – 1.0

    synth.startSpeakingString_(text)

    # keep the script alive until speech is finished
    while synth.isSpeaking():
        time.sleep(0.1)

def listen():
    """Continuously listens for commands in the background."""
    global is_listening

    while is_listening:
        with sr.Microphone() as source:
            print("🎤 Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = recognizer.listen(source, phrase_time_limit=5)
                text = recognizer.recognize_google(audio).lower()
                print(text)

                if "jarvis" in text:  # Only process if wake word is detected
                    print("Working!")
                    output = chat(text)
                    print(f"🤖 {output}")
                    say_text(output)
                    # engine.say(output)
                    # engine.runAndWait()
            except sr.UnknownValueError:
                pass  # Ignore unrecognized speech
            except sr.RequestError:
                print("⚠️ Speech recognition service unavailable.")
            except Exception as e:
                print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    listen()