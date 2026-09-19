import threading

import speech_recognition as sr

from dashboard import Dashboard
from voice import VoiceEngine
from gemini_brain import GeminiBrain


class Avni:

    def __init__(self):

        self.dashboard = Dashboard()

        self.voice = VoiceEngine()

        self.brain = GeminiBrain()

        self.running = True

        # Start voice engine in background
        threading.Thread(
            target=self.voice_loop,
            daemon=True
        ).start()

    def set_state(self, state):

        self.dashboard.root.after(
            0,
            lambda: self.dashboard.set_state(state)
        )

    def voice_loop(self):

        microphone = sr.Microphone()

        self.voice.calibrate(microphone)

        while self.running:

            print("\nListening for: Hey Avni...")

            self.dashboard.set_state("LISTENING")

            text = self.voice.listen(microphone)

            print("Heard:", repr(text))

            # Wake word detected
            if self.voice.is_wake_word(text):

                print("Wake word detected!")

                # Avni responds every time
                self.dashboard.set_state("SPEAKING")
                self.voice.speak("Yes Roushan, How Can I help you?")

                print("Listening for your command...")

                self.dashboard.set_state("LISTENING")

                command = self.voice.listen(microphone)

                print("Command received:", repr(command))

                if not command:

                    self.dashboard.set_state("SPEAKING")
                    self.voice.speak("I didn't hear your command.")

                    self.dashboard.set_state("IDLE")

                    continue

                self.dashboard.set_state("THINKING")

                print("Sending to Gemini:", command)

                try:

                    response = self.brain.ask(command)

                    print("Gemini response:", response)

                    self.dashboard.set_state("SPEAKING")

                    self.voice.speak(response)

                except Exception as error:

                    print("Gemini error:", error)

                    self.dashboard.set_state("SPEAKING")

                    self.voice.speak(
                        "Sorry, I couldn't connect to Gemini."
                    )

                # Return to wake-word listening
                self.dashboard.set_state("IDLE")

                print("\nReady for next 'Hey Avni'...")

                continue

            self.dashboard.set_state("IDLE")
    def run(self):

        self.dashboard.run()


if __name__ == "__main__":

    app = Avni()

    app.run()