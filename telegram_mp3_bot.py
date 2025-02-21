import telebot
import yt_dlp
import os

# FFmpeg yolunu manuel olarak ekleyelim (Windows kullanıcıları için gerekli olabilir)
os.environ["PATH"] += os.pathsep + "C:\ffmpeg\bin"

# Telegram Bot API Token
TOKEN = "8196635991:AAG9703J6DJ0qxUDcOBWgq4Qgfjg65Zt_wg"  # Buraya kendi tokenini ekle
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "MP3 indirme botuna xoş gəldiniz! YouTube linkini göndərin.")

@bot.message_handler(func=lambda message: True)
def download_audio(message):
    url = message.text
    chat_id = message.chat.id

    bot.send_message(chat_id, "MP3 hazırlanır, biraz gözləyin...")

    # MP3 indirme ayarları
    ydl_opts = {
        'format': 'bestaudio/best',
        'ffmpeg_location': "/usr/bin/ffmpeg",  # Eğer hata alırsan burayı FFmpeg'in kurulu olduğu dizinle değiştir
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'downloaded_song.%(ext)s'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # MP3 dosyasını bul
        mp3_file = None
        for file in os.listdir():
            if file.startswith("downloaded_song") and file.endswith(".mp3"):
                mp3_file = file
                break

        if mp3_file:
            # MP3 dosyasını Telegram'a göndər
            with open(mp3_file, "rb") as audio:
                bot.send_audio(chat_id, audio)

            os.remove(mp3_file)  # MP3 dosyasını sil
        else:
            bot.send_message(chat_id, "MP3 faylı tapılmadı!")

    except Exception as e:
        bot.send_message(chat_id, f"Xəta baş verdi: {str(e)}")

bot.polling()
