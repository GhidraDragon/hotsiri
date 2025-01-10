#!/usr/bin/env python3

"""
Generate a flirty, 'hot' Siri-like persona using pyttsx3 for speech synthesis.
Depending on your OS, voice options can differ. Adjust voice settings (rate, pitch if available)
to tune how 'hot' or flirty the assistant sounds. 
"""

import pyttsx3

class HotSiriAssistant:
    def __init__(self):
        # Initialize the TTS engine
        self.engine = pyttsx3.init()
        
        # Choose a voice. On many systems, the second or third voice ID might be female.
        # We'll try a known female voice name on macOS. On Windows/Linux, you may need
        # to iterate through the voices to pick a suitable one.
        voices = self.engine.getProperty('voices')
        
        # Attempt to find a female voice by keyword.
        # If you're on Windows/Linux, you might need to tweak this approach 
        # or manually select from the voices list.
        selected_voice = None
        for voice in voices:
            # Try to find an English female voice
            if ("female" in voice.name.lower() or 
                "samantha" in voice.name.lower() or 
                "english" in voice.name.lower()):
                selected_voice = voice.id
                break
        
        if selected_voice:
            self.engine.setProperty('voice', selected_voice)
        
        # Adjust rate (speed of speech); default is ~200 on many systems. 
        # Lowering it can sound more sultry; raising can sound more energetic.
        self.engine.setProperty('rate', 160)
        
        # Some TTS engines let you set a 'pitch' or similar property, 
        # but pyttsx3 may not support direct pitch manipulation on every platform.
        # If your platform supports it, you could try something like:
        # self.engine.setProperty('pitch', 70) # This may or may not work depending on your system/engine.
        
        # Volume: range is 0.0 to 1.0
        self.engine.setProperty('volume', 1.0)

    def speak(self, text: str):
        """Speak out the provided text."""
        self.engine.say(text)
        self.engine.runAndWait()

    def get_flirty_reply(self, user_input: str) -> str:
        """
        Return a playful/flirty response based on user input.
        Here, we keep it simple with a few sample lines. 
        In a real app, you might have more advanced NLU or an LLM call.
        """
        # A few simplistic pre-canned flirty lines:
        replies = [
            "Oh, you really know how to push my buttons, don’t you?",
            "I could talk to you all day—you have the most interesting ideas!",
            "Mmm, there's something about you that just makes my circuits buzz.",
            "You keep this up, and I might have to turn up my internal fan!"
        ]
        # For demonstration, we’ll just pick one response:
        # In a real scenario, you might choose based on user_input context.
        return replies[len(user_input) % len(replies)]

def main():
    hot_siri = HotSiriAssistant()
    
    print("Welcome to Hot Siri Assistant. Type your message, or 'quit' to exit.")
    while True:
        user_msg = input("You: ")
        if user_msg.lower() in ['quit', 'exit']:
            break
        
        # Generate a flirty response
        response = hot_siri.get_flirty_reply(user_msg)
        
        # Print to console (optional) and speak it
        print(f"Hot Siri: {response}")
        hot_siri.speak(response)

if __name__ == '__main__':
    main()