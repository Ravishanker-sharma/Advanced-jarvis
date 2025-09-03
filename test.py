import AppKit
import time

def list_voices():
    """List all available voices with human-readable names."""
    voices = AppKit.NSSpeechSynthesizer.availableVoices()
    for v in voices:
        attrs = AppKit.NSSpeechSynthesizer.attributesForVoice_(v)
        print(f"ID: {v}")
        print(f"  Name     : {attrs.get('VoiceName')}")
        print(f"  Language : {attrs.get('VoiceLocaleIdentifier')}")
        print(f"  Gender   : {attrs.get('VoiceGender')}")
        print(f"  Age      : {attrs.get('VoiceAge')}")
        print("-" * 40)

def say_text(text, voice=None, rate=175, volume=1.0):
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

if __name__ == "__main__":
    print("🔊 Available voices on your Mac:\n")
    list_voices()

    print("\n✅ Example: speaking with Rishi (Enhanced, if installed)\n")
    say_text(
        "Hello Ravi, this is the enhanced Rishi voice speaking smoothly!",
        voice="com.apple.voice.compact.en-IN.Rishi",  # change this to any ID from list_voices()
        rate=175,
        volume=0.9
    )
