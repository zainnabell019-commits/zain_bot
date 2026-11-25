import os
from threading import Thread
from flask import Flask
from bot import run_bot

app = Flask(__name__)

@app.route('/')
def home():
    return "Zain Academy Bot is alive and running!"

def start_bot():
    run_bot()

if __name__ == "__main__":
    # تشغيل البوت في الخلفية
    t = Thread(target=start_bot)
    t.start()
    
    # تشغيل السيرفر الوهمي عشان Koyeb يقبل التشغيل
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
