import time
import json
import os
import requests
from datetime import date, datetime
try:
    from gtts import gTTS
except ImportError:
    os.system("pip install gtts requests")
    from gtts import gTTS
TELEGRAM_TOKEN = "8701935180:AAGiOmID8vwOK8DNVGNAJNc5vchEOkTXip8"
CHAT_ID        = "1045515367"
STREAK_FILE = "study_streak.json"
STUDY_TOPICS = [
    "Python programming and data structures",
    "Machine learning and AI concepts",
    "Web development with HTML CSS and JavaScript",
    "Mathematics and problem solving",
    "English communication skills",
    "Data science and analytics",
    "Computer networking basics",
    "Database and SQL fundamentals",
    "Operating systems concepts",
    "Algorithms and competitive programming",
]
def load_streak():
    if os.path.exists(STREAK_FILE):
        with open(STREAK_FILE, "r") as f:
            return json.load(f)
    return {"streak": 0, "last_date": "", "total_days": 0}
def save_streak(data):
    with open(STREAK_FILE, "w") as f:
        json.dump(data, f, indent=2)
def update_streak():
    data = load_streak()
    today = str(date.today())
    if data["last_date"] == today:
        return data
    yesterday = str(date.fromordinal(date.today().toordinal() - 1))
    if data["last_date"] == yesterday:
        data["streak"] += 1
    else:
        data["streak"] = 1
    data["last_date"] = today
    data["total_days"] += 1
    save_streak(data)
    return data
def get_topic_of_day():
    day_index = date.today().toordinal() % len(STUDY_TOPICS)
    return STUDY_TOPICS[day_index]
def send_telegram_text(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("Text message sent!")
    else:
        print(f"Failed: {response.text}")
def send_telegram_voice(message):
    voice_file = "study_alarm.mp3"
    tts = gTTS(text=message, lang="en", slow=False)
    tts.save(voice_file)
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendVoice"
    with open(voice_file, "rb") as audio:
        response = requests.post(url, data={"chat_id": CHAT_ID}, files={"voice": audio})
    if response.status_code == 200:
        print("Voice message sent!")
    else:
        print(f"Failed: {response.text}")
    if os.path.exists(voice_file):
        os.remove(voice_file)
def study_alarm():
    print(f"Alarm triggered at {datetime.now()}")
    data = update_streak()
    topic = get_topic_of_day()
    streak = data["streak"]
    total = data["total_days"]
    if streak == 1:
        streak_msg = "Day 1 of your streak. Great start!"
    elif streak < 7:
        streak_msg = f"{streak} days in a row. Keep going!"
    elif streak < 30:
        streak_msg = f"Amazing! {streak} day streak. You are on fire!"
    else:
        streak_msg = f"Incredible! {streak} days non-stop!"
    voice_message = (
        f"Hey Senthil! It is 8 PM. Time to study! "
        f"Today's topic is {topic}. "
        f"{streak_msg} "
        f"You have studied for {total} days total. "
        f"Open your books now. Lets go!"
    )
    text_message = (
        f"Study Reminder!\n\n"
        f"Time: 8:00 PM\n"
        f"Topic: {topic}\n"
        f"Streak: {streak} day(s)\n"
        f"Total studied: {total} day(s)\n\n"
        f"{streak_msg}\n\n"
        f"Open your books and lets go!"
    )
    send_telegram_text(text_message)
    time.sleep(1)
    send_telegram_voice(voice_message)
print(f"Agent started at {datetime.now()}")
print("Waiting for 8:00 PM...")
last_triggered = ""
while True:
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    
    if current_time == "11:45" and last_triggered != current_time:
        last_triggered = current_time
        study_alarm()
    
    print(f"Checking time: {current_time}")
    time.sleep(55)

when i will get msg
