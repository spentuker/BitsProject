from fastapi import FastAPI, File, UploadFile
import speech_recognition as sr
import pyttsx3
from text_extract import extract_text
import spacy
import re
import io

app = FastAPI()

nlp = spacy.load("en_core_web_sm")

engine = pyttsx3.init()

messages = [{"role": "system",
             "content": "You are a medical assistant bot. Provide brief, concise answers ONLY to medical questions. If a user asks a non-medical question, respond with 'Please ask a medical question.' Keep responses under 100 words."
             }]

@app.get("/")
def home():
    return {"message": "Medical Chatbot API is Running!"}

@app.post("/process-audio/")
async def process_audio(file: UploadFile = File(...)):
    recognizer = sr.Recognizer()
    
    try:
        # Read the audio file
        audio_data = await file.read()
        audio_file = io.BytesIO(audio_data)

        # Convert audio file to speech recognition format
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)

        # Recognize text from speech
        text = recognizer.recognize_google(audio)
        personal_info(text)

        if text.lower() in ["quit", "exit", "bye", "thank you"]:
            return {"response": "Medical Chatbot: Goodbye!"}

        res_text = extract_text(messages, text)

        if res_text:
            if "Please ask a medical question." not in res_text:
                messages.append({"role": "assistant", "content": res_text})  # Store response if medical.
            else:
                return {"response": "Medical Chatbot: Please ask a medical question."}
        else:
            res_text = "Sorry, I encountered an error."

        # Speak the response (Optional)
        def speak_text(text):
            engine.say(text)
            engine.runAndWait()

        speak_text(res_text)

        return {"response": res_text}

    except sr.UnknownValueError:
        return {"error": "Could not understand audio"}
    except sr.RequestError as e:
        return {"error": f"Could not request results from Google Speech Recognition service; {e}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}

def personal_info(input_text: str):
    patterns = {
        "name": r"my name is (\w+ \w+)",
        "age": r"I am (\d+) years old",
        "gender": r"I am (\bmale\b|\bfemale\b)",
        "medications": r"I take (.+?) for",
        "allergies": r"I am allergic to (.+?)\.",
        "emergency_contact": r"My emergency contact is (\w+ \w+), my (\w+), at (\+\d+)"
    }

    user_info = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, input_text, re.IGNORECASE)
        if match:
            user_info[key] = match.groups() if len(match.groups()) > 1 else match.group(1)

    doc = nlp(input_text)
    user_info["medical_conditions"] = [ent.text for ent in doc.ents if ent.label_ == "DISEASE"]

    return user_info

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
