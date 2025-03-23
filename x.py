import pymongo
import pytz
from datetime import datetime
from playsound import playsound
from gtts import gTTS
import os

# MongoDB Atlas Connection
MONGO_URI = "mongodb+srv://nishit:seekhan@cluster0.u6w2n.mongodb.net/aushadTrail"
DB_NAME = "aushadsecondT"
COLLECTION_NAME = "medicines"

# Connect to MongoDB Atlas
client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]
medicines_collection = db[COLLECTION_NAME]

# Define IST Time Zone
IST = pytz.timezone("Asia/Kolkata")

def fetch_active_medicines():
    """Fetch all active medicines from MongoDB."""
    return list(medicines_collection.find({"status": "active"}))

def speak_reminder(text):
    """Convert text to speech and play the reminder audio."""
    try:
        tts = gTTS(text=text, lang="en")
        tts.save("reminder.mp3")
        playsound("reminder.mp3")
        os.remove("reminder.mp3")
    except Exception as e:
        print(f"❌ Error playing reminder: {e}")

def check_medicine_times():
    """Continuously checks for medicine time for all documents."""
    print("📡 Medicine Reminder is running...")

    last_checked_time = None  # Store last checked time to avoid duplicate alerts

    while True:
        now = datetime.now(IST)  # Get current time in IST
        current_time_str = now.strftime("%H:%M")  # Format as HH:MM (ignores seconds)

        if current_time_str != last_checked_time:  # Check only when the minute changes
            medicines = fetch_active_medicines()  # Fetch all medicines
            due_medicines = []  # List to collect medicines due now

            for med in medicines:
                medicine_name = med.get("medicine_name")
                dose_time = med.get("dose_time")  # Expected format: "HH:MM"

                if dose_time == current_time_str:  # Compare only HH:MM
                    due_medicines.append(medicine_name)  # Add to list

            # If medicines are due, announce them all together
            if due_medicines:
                reminder_text = f"🔔 Time to take your medicines: {', '.join(due_medicines)}."
                print(reminder_text)
                speak_reminder(reminder_text)

            # Print traversal complete message
            print(f"✅ {current_time_str} - Traversal Complete")

            last_checked_time = current_time_str  # Update last checked time

if __name__ == "__main__":
    check_medicine_times()
