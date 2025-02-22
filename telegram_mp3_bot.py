import os
import telebot
from pytube import YouTube
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salam! YouTube linkini göndərin, mən isə MP3 faylını sizə göndərim.")

@bot.message_handler(func=lambda message: True)
def download_audio(message):
    url = message.text
    if "youtube.com" in url or "youtu.be" in url:
        try:
            bot.reply_to(message, "Yükləmə başlayır, bir az gözləyin...")
            yt = YouTube(url)
            audio_stream = yt.streams.filter(only_audio=True).first()
            audio_file = audio_stream.download(filename=f"{yt.title}.mp3")

            with open(audio_file, "rb") as audio:
                bot.send_audio(message.chat.id, audio)

            os.remove(audio_file)
        except Exception as e:
            bot.reply_to(message, f"Xəta baş verdi: {e}")
    else:
        bot.reply_to(message, "Lütfən, düzgün bir YouTube linki göndərin.")

print("Bot işə düşdü")
bot.polling()}
