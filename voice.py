import threading
import speech_recognition as sr
import pyttsx3

from config import WAKE_PHRASES


class VoiceEngine:

    def __init__(self):

        # =========================
        # SPEECH RECOGNITION
        # =========================

        self.recognizer = sr.Recognizer()
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.7

        # =========================
        # TEXT TO SPEECH
        # =========================

        self.tts_lock = threading.Lock()

        self.tts = pyttsx3.init()

        self.tts.setProperty("rate", 165)
        self.tts.setProperty("volume", 1.0)

        # =========================
        # FEMALE ENGLISH VOICE
        # =========================

        voices = self.tts.getProperty("voices")

        zira_voice = None

        for voice in voices:

            if "zira" in (voice.name or "").lower():
                zira_voice = voice
                break

        if zira_voice:

            self.tts.setProperty(
                "voice",
                zira_voice.id
            )

            print(
                "Female voice selected:",
                zira_voice.name
            )

        else:

            print("Microsoft Zira voice not found.")

    # =========================
    # MICROPHONE CALIBRATION
    # =========================

    def calibrate(self, microphone):

        print("Calibrating microphone...")

        with microphone as source:

            self.recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

        print("Microphone ready.")

    # =========================
    # LISTEN
    # =========================

    def listen(self, microphone):

        with microphone as source:

            print("Listening...")

            audio = self.recognizer.listen(
                source,
                phrase_time_limit=8
            )

        try:

            text = self.recognizer.recognize_google(
                audio,
                language="en-US"
            )

            print("You:", text)

            return text.strip()

        except sr.UnknownValueError:

            print("Could not understand audio.")

            return ""

        except sr.RequestError as error:

            print("Speech recognition error:", error)

            return ""

    # =========================
    # WAKE WORD
    # =========================

    def is_wake_word(self, text):

        normalized = " ".join(
            text.lower().strip().split()
        )

        print("Checking wake word:", repr(normalized))

        for phrase in WAKE_PHRASES:

            if normalized == phrase:

                print(
                    "Wake phrase matched:",
                    phrase
                )

                return True

        return False

    # =========================
    # SPEAK
    # =========================

    def speak(self, text):

        if not text:
            print("TTS: Empty response")
            return

        print("TTS RECEIVED:", repr(text))

        try:

            with self.tts_lock:

                # Create a fresh TTS engine
                engine = pyttsx3.init()

                engine.setProperty("rate", 165)
                engine.setProperty("volume", 1.0)

                # Select Microsoft Zira
                for voice in engine.getProperty("voices"):

                    if "zira" in (voice.name or "").lower():

                        engine.setProperty(
                            "voice",
                            voice.id
                        )

                        print(
                            "Using voice:",
                            voice.name
                        )

                        break

                print("TTS STARTING...")

                engine.say(text)

                engine.runAndWait()

                engine.stop()

                print("TTS FINISHED")

        except Exception as error:

            print("TTS ERROR:", repr(error))