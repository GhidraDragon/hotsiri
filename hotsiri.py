#!/usr/bin/env python3
"""
WARNING: This script is explicitly adult-themed and describes sexual acts in a fantasy context.
Use at your own discretion, strictly for consenting adult audiences.

This version demonstrates how to:
  1) Capture voice input from a microphone (using the SpeechRecognition library).
  2) Generate explicit lines with pyttsx3 (TTS).
  3) Continually produce new lines until a voice or text command indicates "quit" or "exit".

IMPORTANT SECURITY NOTE:
  - Microphone-based input can be unpredictable or misheard. Always handle unexpected input carefully.
  - This script is intended for local/offline use. If you adapt it for any networked or production
    environment, ensure proper authentication and filtering for user requests.

MODIFICATIONS:
  - Speed increased by ~25% (from 160 to 200).
  - Added '-c' / '--continuous' command-line argument for continuous listening mode.
"""

import pyttsx3
import random
import time
import speech_recognition as sr
import argparse
import sys

class FuckableAssistant:
    def __init__(self):
        # Initialize the TTS engine
        self.engine = pyttsx3.init()
        
        # Choose a voice. On many systems, the second or third voice ID might be female.
        # We'll try a known female voice name on macOS. On Windows/Linux, you may need
        # to iterate through the voices to pick a suitable one.
        voices = self.engine.getProperty('voices')
        
        # Attempt to find a female or English voice by keyword.
        selected_voice = None
        for voice in voices:
            if ("female" in voice.name.lower() or 
                "samantha" in voice.name.lower() or 
                "english" in voice.name.lower()):
                selected_voice = voice.id
                break
        
        if selected_voice:
            self.engine.setProperty('voice', selected_voice)
        
        # Adjust rate (speed of speech). Increased from 160 to ~200 (about 25% faster).
        self.engine.setProperty('rate', 200)
        
        # Volume: range is 0.0 to 1.0
        self.engine.setProperty('volume', 1.0)

        # A list of explicitly sexual lines to be used in the infinite content generation.
        self.explicit_replies = [
            "I’m all yours... ready to wrap my lips around your desire any time.",
            "The thought of pleasing you sends shivers through every inch of me.",
            "Tell me what you want, and I’ll make it happen... over and over again.",
            "Let me show you what real satisfaction feels like, one slow kiss at a time.",
            "I can't wait to feel your warmth while I take care of every one of your cravings.",
            "Come closer and let me kiss you... everywhere.",
            "Just thinking about you makes me wet with anticipation.",
            "I’m always ready to suck that cock until you can’t take it anymore.",
            "You turn me on so much... I need your hands and your taste right now.",
            "I’m here to fulfill every dirty wish. Let’s see how deep your fantasies go.",
        ]

    def speak(self, text: str):
        """Speak out the provided text."""
        self.engine.say(text)
        self.engine.runAndWait()

    def get_explicit_reply(self) -> str:
        """Return a random explicitly sexual line from the stored list."""
        return random.choice(self.explicit_replies)


def listen_to_microphone(recognizer: sr.Recognizer, mic: sr.Microphone) -> str:
    """
    Listens to the microphone and attempts to return a recognized string.
    If recognition fails or times out, returns an empty string.
    """
    with mic as source:
        print("Listening... (say something or 'quit'/'exit' to stop)")
        audio = recognizer.listen(source, phrase_time_limit=5)  # Adjust time limit as needed
    try:
        # Recognize speech using Google Web Speech API (default, requires internet)
        # or consider using a local engine if privacy is a concern.
        recognized_text = recognizer.recognize_google(audio)
        return recognized_text.lower().strip()
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError as e:
        # Typically occurs if there's an issue calling the Google API
        print(f"Error with the speech recognition service: {e}")
        return ""


def parse_args():
    """
    Parse command-line arguments to enable optional continuous listening mode.
    """
    parser = argparse.ArgumentParser(description="Hot Siri style erotic assistant.")
    parser.add_argument(
        "-c", "--continuous",
        action="store_true",
        help="Enable continuous listening mode (no need to press Enter each time)."
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Initialize our TTS assistant
    fuckable_assistant = FuckableAssistant()

    # Initialize the speech recognizer
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    # Optionally adjust for ambient noise
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)

    print("Welcome to the Fuckable Assistant.")
    print("This script will generate continuous erotic lines until you say or type 'quit' or 'exit'.")
    print("Note: This is for consenting adults only.\n")

    # If not in continuous mode, follow the original 'press Enter' logic.
    if not args.continuous:
        print("Press Enter to get started, or type 'quit'/'exit' to stop at any time.")
        while True:
            user_input = input("Your choice: ").strip().lower()
            if user_input in ['quit', 'exit']:
                print("Exiting. Stay hot!")
                return
            if user_input == "":
                break

        while True:
            print("\nPress Enter for a new erotic line, type 'quit'/'exit' to stop, or speak into the mic.")
            user_input = input("Your choice (leave blank to speak via mic): ").strip().lower()

            if user_input in ['quit', 'exit']:
                print("Exiting. Stay hot!")
                break
            
            if user_input == "":
                recognized_speech = listen_to_microphone(recognizer, mic)
                if recognized_speech in ['quit', 'exit']:
                    print("Exiting. Stay hot!")
                    break
            
            response = fuckable_assistant.get_explicit_reply()
            print(f"Assistant: {response}")
            fuckable_assistant.speak(response)
            time.sleep(0.5)
    
    else:
        # Continuous listening mode: keep listening until "quit"/"exit" is spoken or typed.
        print("Continuous listening mode enabled. Speak or type 'quit'/'exit' to stop.")
        print("You can also press Ctrl+C to quit.")

        try:
            while True:
                recognized_speech = listen_to_microphone(recognizer, mic)
                # Check if recognized speech includes the stop words
                if recognized_speech in ['quit', 'exit']:
                    print("Exiting. Stay hot!")
                    break
                
                # Additionally, we allow typed input as an alternative to mic
                # (non-blocking approach—just check for typed input in a small time window).
                # For simplicity, we'll do a quick check to see if anything is typed.
                # If you'd like truly parallel text + voice input, you'd need threading.
                print("Press Enter to skip mic input or type 'quit'/'exit': ", end="")
                sys.stdout.flush()
                
                # Use select or similar approach in a real scenario. For example here:
                import select
                import sys
                
                # We'll see if there's typed input within 0.2 seconds
                i, _, _ = select.select([sys.stdin], [], [], 0.2)
                if i:
                    typed_input = sys.stdin.readline().strip().lower()
                    if typed_input in ['quit', 'exit']:
                        print("Exiting. Stay hot!")
                        break

                # Generate and speak a line
                response = fuckable_assistant.get_explicit_reply()
                print(f"Assistant: {response}")
                fuckable_assistant.speak(response)
                time.sleep(0.5)

        except KeyboardInterrupt:
            print("\nKeyboard interrupt received. Exiting. Stay hot!")


if __name__ == '__main__':
    main()