import os
import telebot
import subprocess
from telebot import types

# Telegram Bot Tokeninizi buraya əlavə edin
BOT_TOKEN = os.getenv("BOT_TOKEN", "8196635991:AAG9703J6DJ0qxUDcOBWgq4Qgfjg65Zt_wg")

# Bot obyektini yaradın
bot = telebot.TeleBot(BOT_TOKEN)

# Start komandası
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "👋 Salam! YouTube videolarını MP3 formatında yükləmək üçün link göndərin.")

# MP3 yükləmə funksiyası
def download_mp3(url):
    output_path = "downloads"
    os.makedirs(output_path, exist_ok=True)

    # MP3 faylının saxlanacağı yer
    output_file = os.path.join(output_path, "%(title)s.%(ext)s")

    # yt-dlp əmrini qur
    command = [
        "yt-dlp",
        "--extract-audio",
        "--audio-format", "mp3",
        "--cookies", "cookies.txt",  # Cookie faylınız
        "-o", output_file,
        url
    ]

    try:
        # Əmri icra et
        subprocess.run(command, check=True)
        # Yüklənən faylı tapın
        for file in os.listdir(output_path):
            if file.endswith(".mp3"):
                return os.path.join(output_path, file)
        return None
    except subprocess.CalledProcessError as e:
        print(f"Xəta baş verdi: {e}")
        return None

# Mesaj alanda işləyən funksiya
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text.strip()

    if "youtube.com" in url or "youtu.be" in url:
        bot.reply_to(message, "🎵 MP3 yüklənir, bir az gözləyin...")
        mp3_file = download_mp3(url)

        if mp3_file:
            with open(mp3_file, "rb") as audio:
                bot.send_audio(message.chat.id, audio)
            os.remove(mp3_file)  # Faylı göndərdikdən sonra silin
        else:
            bot.reply_to(message, "❌ Yükləmə zamanı xəta baş verdi.")
    else:
        bot.reply_to(message, "🚫 Zəhmət olmasa etibarlı YouTube linki göndərin.")

# Botu işə salın
print("🤖 Bot işə düşdü...")
bot.polling(non_stop=True, drop_pending_updates=True)
