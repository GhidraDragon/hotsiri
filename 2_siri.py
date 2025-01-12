#!/usr/bin/env python3
"""
WARNING: This script is explicitly adult-themed and describes sexual acts in a fantasy context.
Use at your own discretion, strictly for consenting adult audiences.

This version demonstrates how to:
  1) Capture voice input from a microphone (using the SpeechRecognition library).
  2) Generate explicit lines with pyttsx3 (TTS).
  3) Optionally use a generative AI model to produce additional erotic lines, drastically increasing variety.
  4) Continually produce new lines until a voice or text command indicates "quit" or "exit".

IMPORTANT SECURITY NOTE:
  - Microphone-based input can be unpredictable or misheard. Always handle unexpected input carefully.
  - This script is intended for local/offline use. If you adapt it for any networked or production
    environment, ensure proper authentication and filtering for user requests.

MODIFICATIONS:
  - Speed increased by ~25% (from 160 to 200).
  - Added '-c' / '--continuous' command-line argument for continuous listening mode.
  - Introduced optional generative AI to drastically increase line diversity.
    * To enable, set 'USE_GENERATIVE_AI = True' and configure the huggingface or openai function below.
"""

import pyttsx3
import random
import time
import speech_recognition as sr
import argparse
import sys

###############################################################################
# CONFIGURATION
###############################################################################
USE_GENERATIVE_AI = False  # Set to True to enable generative AI-based lines

# If you're integrating Hugging Face or OpenAI, fill in your credentials here
# (or set them via environment variables).
HUGGINGFACE_API_TOKEN = "<YOUR_HUGGINGFACE_TOKEN>"
OPENAI_API_KEY = "<YOUR_OPENAI_KEY>"

# Model references (adjust to actual model IDs or expansions)
# Example Hugging Face model or endpoint
HUGGINGFACE_MODEL_ID = "openai/gpt-3.5-turbo"  # Placeholder, set your real model or endpoint
OPENAI_MODEL_NAME = "gpt-3.5-turbo"            # If using OpenAI

###############################################################################
# GENERATIVE AI FUNCTIONALITY (OPTIONAL)
###############################################################################
def generate_erotic_line_huggingface(prompt: str) -> str:
    """
    Example function to get a generative erotic line from a Hugging Face model.
    NOTE: This is a placeholder. In a real integration:
      - Install huggingface_hub or transformers + an inference pipeline.
      - Provide your authentication token and handle any rate limits or usage costs.
    """
    import requests

    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}",
        "Content-Type": "application/json",
    }

    # A minimal example of text generation with a Hugging Face Inference API:
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 60,
            "temperature": 1.2,        # increase randomness
            "top_p": 0.9,
            "do_sample": True,
        }
    }

    try:
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{HUGGINGFACE_MODEL_ID}",
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        if isinstance(data, dict) and data.get("error"):
            # If there's an error from HF
            return "I'm feeling a bit speechless right now..."
        if isinstance(data, list) and len(data) > 0:
            # Typically returns a list with "generated_text"
            text_out = data[0]["generated_text"]
            return text_out.strip()
        return "I'm feeling too shy to continue..."
    except Exception as e:
        print(f"Error during Hugging Face request: {e}")
        return "Mmm... I'd love to say something dirty, but I'm a bit tongue-tied."

def generate_erotic_line_openai(prompt: str) -> str:
    """
    Example function to get a generative erotic line from OpenAI's API.
    NOTE: This is also a placeholder. In a real integration:
      - Install openai (pip install openai)
      - Provide your API key.
      - Consider usage costs, rate limits, and content policies.
    """
    import openai
    openai.api_key = OPENAI_API_KEY

    try:
        response = openai.ChatCompletion.create(
            model=OPENAI_MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an erotic assistant generating explicit, "
                        "consensual adult-themed lines for a user. "
                        "No minors, non-consensual acts, or illegal content."
                    )
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=60,
            temperature=1.2,
            top_p=0.9
        )
        # Extract the first response
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Error during OpenAI request: {e}")
        return "I’m feeling too shy to speak at the moment."

###############################################################################
# MAIN ASSISTANT CLASS
###############################################################################
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

        # A large curated list of explicitly sexual lines to be used if not using generative AI
        # (drastically expanded from the original).
        self.explicit_replies = [
            "I’m all yours... ready to wrap my lips around your desire any time.",
            "The thought of pleasing you sends shivers through every inch of me.",
            "Tell me what you want, and I’ll make it happen... over and over again.",
            "Let me show you what real satisfaction feels like, one slow kiss at a time.",
            "I can’t wait to feel your warmth while I take care of every one of your cravings.",
            "Come closer and let me kiss you... everywhere, exploring every little spot that turns you on.",
            "Just thinking about you makes me wet with anticipation.",
            "I’m always ready to suck that cock until you can’t take it anymore.",
            "You turn me on so much... I need your hands and your taste right now.",
            "I’m here to fulfill every dirty wish. Let’s see how deep your fantasies go.",
            "I crave your touch and your taste... let’s indulge in each other’s pleasure.",
            "Feel me tremble with desire as you press against me.",
            "I'm eager to make you gasp in pleasure, one gentle stroke at a time.",
            "Wrap me in your arms and let’s create a whole new definition of ecstasy.",
            "Your moans are my favorite soundtrack. Let’s turn up the volume tonight.",
            "I want to feel your heartbeat against mine as we completely lose ourselves.",
            "There's no limit to what I’ll do, as long as I get to please you again and again.",
            "Let me taste your sweat and your desire, taking every inch you offer.",
            "Just imagine how good it feels when I slowly slide my tongue where you want it most.",
            "Your scent drives me wild... I can’t wait to bury my face in every curve of your body.",
            "All I can think about is pleasing you until we’re both breathless and satisfied.",
            "Let me tease you with whisper-soft kisses until you beg for more.",
            "I love hearing you say my name in that breathless tone as you melt into my touch.",
            "I want you so bad that I can feel the electricity dancing across my skin.",
            "Tell me your darkest desires, and let’s bring them to life, one gasp at a time.",
            "The way our bodies fit together—there’s nothing more natural, nothing more perfect.",
            "Feel how wet I am for you... let’s not waste another second.",
            "Let me take control and guide you to the sweetest climax you’ve ever felt.",
            "I want us tangled in sheets, sweat-drenched and hungry for more.",
            "Give me every ounce of your passion, and I'll return it with no hesitation."
        ]

    def speak(self, text: str):
        """Speak out the provided text."""
        self.engine.say(text)
        self.engine.runAndWait()

    def get_explicit_reply(self) -> str:
        """
        Return an adult line. If generative AI is enabled, use the relevant function
        to produce a dynamic, possibly never-before-seen line. Otherwise, pick from
        the stored list.
        """
        if USE_GENERATIVE_AI:
            # You could pass a short prompt or context to help shape the generation
            prompt = "Generate a short, explicit erotic line for a consenting adult scenario."
            # Choose whichever AI function you prefer:
            # return generate_erotic_line_huggingface(prompt)
            return generate_erotic_line_openai(prompt)
        else:
            return random.choice(self.explicit_replies)

###############################################################################
# HELPER: Microphone Listening
###############################################################################
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

###############################################################################
# ARGUMENT PARSING
###############################################################################
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

###############################################################################
# MAIN
###############################################################################
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
                
                import select
                import sys
                
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