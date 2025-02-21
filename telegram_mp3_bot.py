import os
import telebot
import yt_dlp

# Environment dəyişkənindən Token almaq
TOKEN = os.getenv("8196635991:AAG9703J6DJ0qxUDcOBWgq4Qgfjg65Zt_wg")
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN tapılmadı. Environment dəyişkənini yoxla!")

bot = telebot.TeleBot(TOKEN)

# Start komandası
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Salam! İstədiyiniz YouTube linkini göndərin, mən MP3 şəklində endirim. 🎵")

# Link göndəriləndə
@bot.message_handler(func=lambda message: message.text.startswith("http"))
def download_audio(message):
    url = message.text
    bot.reply_to(message, "MP3 hazırlanır... ⏳")

    # Unikal fayl adı yaratmaq üçün istifadəçinin chat ID-sindən istifadə edirik
    file_name = f"downloads/audio_{message.chat.id}.mp3"

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': file_name,
        'ffmpeg_location': '/usr/bin/ffmpeg',  # FFMPEG-in yolunu Render serverində yoxla!
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        with open(file_name, "rb") as audio:
            bot.send_audio(message.chat.id, audio)

        # Faylı sil
        if os.path.exists(file_name):
            os.remove(file_name)

    except yt_dlp.utils.DownloadError as e:
        bot.reply_to(message, f"Video yüklənə bilmədi: {str(e)}")
    except Exception as e:
        bot.reply_to(message, f"Naməlum xəta baş verdi: {str(e)}")

# Botu işə sal
print("Bot işləyir...")
bot.polling()
