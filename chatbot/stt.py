import speech_recognition as sr
import pyttsx3
from text_extract import extract_text  # Import the corrected extract_text function
import spacy
import re

def audio_to_speech():
    recognizer = sr.Recognizer()
    engine = pyttsx3.init()

    messages = [{"role": "system",
                 "content": "You are a medical assistant bot. Provide brief, concise answers ONLY to medical questions. If a user asks a non-medical question, respond with 'Please ask a medical question.' Keep responses under 100 words."
                 }]

    try:
        while True:
            with sr.Microphone() as source:
                print("Speak now...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=10)

            print("Recognizing...")
            text = recognizer.recognize_google(audio)
            print(text)
            if text.lower() in ["quit", "exit", "bye","thank you"]:
                print("Medical Chatbot: Goodbye!")
                break

            res_text = extract_text(messages,text)
            
            if res_text:
                if "Please ask a medical question." not in res_text:
                    messages.append({"role": "assistant", "content": res_text}) #store the response if medical.
                else:
                    print("Medical Chatbot: Please ask a medical question.") #tell the user to ask medical.
            else:
                res_text = "Sorry, I encountered an error."

            def speak_text(text):
                engine.say(text)
                engine.runAndWait()

            speak_text(res_text)

    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
    except TimeoutError:
        print("Timeout: No speech detected.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def personal_info(input):
    nlp = spacy.load("en_core_web_sm")

    # Define regex patterns for key info
    patterns = {
        "name": r"my name is (\w+ \w+)",
        "age": r"I am (\d+) years old",
        "gender": r"I am (\bmale\b|\bfemale\b)",
        "medications": r"I take (.+?) for",
        "allergies": r"I am allergic to (.+?)\.",
        "emergency_contact": r"My emergency contact is (\w+ \w+), my (\w+), at (\+\d+)"
    }

    # Extract data
    user_info = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, input, re.IGNORECASE)
        if match:
            user_info[key] = match.groups() if len(match.groups()) > 1 else match.group(1)

    # Process with spaCy for additional details
    doc = nlp(input)
    user_info["medical_conditions"] = [ent.text for ent in doc.ents if ent.label_ == "DISEASE"]


if __name__ == "__main__":
    audio_to_speech()