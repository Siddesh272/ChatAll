import speech_recognition as sr

recognizer = sr.Recognizer()

def speech_recognition():
    with sr.Microphone() as source:
        print("Listening... (Say 'exit' to quit)")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        user_input = recognizer.recognize_google(audio).lower()
        print("You said:", user_input)
        return user_input
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand.")
        return ""
    except sr.RequestError:
        print("Sorry, I encountered an error while trying to access the Google API.")
        return ""
