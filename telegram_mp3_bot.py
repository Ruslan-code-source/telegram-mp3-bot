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
    bot.reply_to(message, "👋 Salam! İstədiyiniz YouTube linkini göndərin, mən MP3 şəklində endirim. 🎵")

# Link göndəriləndə
@bot.message_handler(func=lambda message: message.text and message.text.startswith("http"))
def download_audio(message):
    url = message.text
    bot.reply_to(message, "MP3 hazırlanır... ⏳")

    # Yükleme parametrləri
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'ffmpeg_location': '/usr/bin/ffmpeg',
        'nocheckcertificate': True,    # SSL sertifikatı yoxlamasını söndürmək
        'quiet': False,
    }

    try:
        # Faylı yüklə
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_name = ydl.prepare_filename(info).replace(info['ext'], 'mp3')

        # MP3 faylını göndər
        if os.path.exists(file_name):
            with open(file_name, "rb") as audio:
                bot.send_audio(message.chat.id, audio)

            # Faylı sil
            os.remove(file_name)
        else:
            bot.reply_to(message, "Xəta: MP3 faylı tapılmadı. ❌")

    except Exception as e:
        bot.reply_to(message, f"⚠️ Xəta baş verdi: {str(e)}")

# Botu işə sal
print("🚀 Bot işləyir...")
bot.polling()
