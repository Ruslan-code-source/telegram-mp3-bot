import telebot
from telebot import types
import yt_dlp
import os

# Telegram bot tokeninizi buraya əlavə edin
BOT_TOKEN = "Sizin_Bot_Tokeniniz"
bot = telebot.TeleBot(8196635991:AAG9703J6DJ0qxUDcOBWgq4Qgfjg65Zt_wg)

# YouTube-dan MP3 yükləmək üçün funksiyalar
YDL_OPTS = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': '%(title)s.%(ext)s',
    'noplaylist': True,
    'cookies': 'cookies.txt'
}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Salam! Yükləmək istədiyiniz YouTube linkini göndərin.")

@bot.message_handler(func=lambda message: True)
def download_audio(message):
    url = message.text
    bot.send_message(message.chat.id, "Yükləmə başlayır, bir az gözləyin...")
    
    try:
        with yt_dlp.YoutubeDL(YDL_OPTS) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info).replace(".webm", ".mp3").replace(".m4a", ".mp3")

        with open(filename, 'rb') as audio:
            bot.send_audio(message.chat.id, audio)

        os.remove(filename)
        bot.send_message(message.chat.id, "Yükləmə uğurla tamamlandı!")

    except Exception as e:
        bot.send_message(message.chat.id, f"Xəta baş verdi: {e}")

bot.polling()
