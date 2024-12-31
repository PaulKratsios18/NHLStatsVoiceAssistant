import pyttsx3
import speech_recognition as sr

def speak(text):
    """Convert text to speech and play it."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def get_audio():
    """Get audio input from microphone and convert to text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
            print(f"Recognized: {said}")
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        except Exception as e:
            print(f"Exception: {e}")

    return said.lower() if said else "" 