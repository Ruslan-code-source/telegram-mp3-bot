import telebot
import os
import subprocess

# Telegram bot tokeninizi buraya daxil edin
BOT_TOKEN = "8196635991:AAG9703J6DJ0qxUDcOBWgq4Qgfjg65Zt_wg"
bot = telebot.TeleBot(BOT_TOKEN)

# Komanda: /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Salam! YouTube linkini göndərin, mən onu MP3 formatına çevirim.")

# Video linkini qəbul edib MP3 formatına çevirmək
@bot.message_handler(func=lambda message: True)
def download_audio(message):
    video_url = message.text.strip()

    if "youtube.com" in video_url or "youtu.be" in video_url:
        bot.reply_to(message, "Yükləmə prosesi başladı, bir az gözləyin...")

        try:
            output_file = f"{message.chat.id}.mp3"
            command = [
                "yt-dlp",
                "--cookies", "cookies.txt",  # Cookies faylını əlavə et
                "-x", "--audio-format", "mp3",
                "-o", output_file,
                video_url
            ]

            subprocess.run(command, check=True)
            with open(output_file, "rb") as audio_file:
                bot.send_audio(message.chat.id, audio_file)

            os.remove(output_file)
        except Exception as e:
            bot.reply_to(message, f"Xəta baş verdi: {e}")
    else:
        bot.reply_to(message, "Zəhmət olmasa düzgün YouTube linki göndərin.")

# Botu işə salmaq
print("Bot işə düşdü...")
bot.polling()
import os
import telebot
import yt_dlp
from dotenv import load_dotenv

# Environment dəyişkənlərini yüklə
load_dotenv()

# Telegram tokeni oxu
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
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
