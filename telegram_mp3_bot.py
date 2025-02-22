import os
import telebot
import yt_dlp
from dotenv import load_dotenv

# Environment dəyişkənlərini yüklə
load_dotenv()

# Telegram tokeni oxu
TOKEN = os.getenv("8196635991:AAG9703J6DJ0qxUDcOBWgq4Qgfjg65Zt_wg")
if not TOKEN:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN tapılmadı. Environment dəyişkənini yoxla!")

bot = telebot.TeleBot(TOKEN)

# Start komandası
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Salam! İstədiyiniz YouTube linkini göndərin, mən MP3 şəklində endirim. 🎵")

# YouTube linki göndəriləndə
@bot.message_handler(func=lambda message: message.text and message.text.startswith("http"))
def download_audio(message):
    url = message.text
    bot.reply_to(message, "MP3 hazırlanır... ⏳")

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'downloaded_audio.%(ext)s',
        'ffmpeg_location': '/usr/bin/ffmpeg',
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        audio_file = "downloaded_audio.mp3"
        with open(audio_file, "rb") as audio:
            bot.send_audio(message.chat.id, audio)

        os.remove(audio_file)

    except Exception as e:
        bot.reply_to(message, f"Xəta baş verdi: {str(e)}")

# Botu işə sal
print("🤖 Bot işləyir...")
bot.polling()
