import os
import telebot
import yt_dlp

# Telegram bot tokenini ortam değişkeninden al
TOKEN = os.getenv("8196635991:AAG9703J6DJ0qxUDcOBWgq4Qgfjg65Zt_wg")
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN bulunamadı. Environment değişkenlerini kontrol et.")

bot = telebot.TeleBot(TOKEN)

# /start komutu
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Salam! YouTube linkini göndər, mən isə MP3 formatında yükləyim. 🎵")

# YouTube linkini işləyən funksiya
@bot.message_handler(func=lambda message: message.text and 'youtube.com' in message.text or 'youtu.be' in message.text)
def download_audio(message):
    url = message.text
    bot.reply_to(message, "Yükləmə başladı... Biraz gözləyin. ⏳")

    # Yükləmə ayarları
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_name = f"downloads/{info['title']}.mp3"
            with open(file_name, 'rb') as audio:
                bot.send_audio(message.chat.id, audio)
        bot.reply_to(message, "Yükləmə uğurla başa çatdı! ✅")
    except Exception as e:
        bot.reply_to(message, f"Xəta baş verdi: {e}")

# Botu işlət
print("Bot işə düşdü...")
bot.polling()
