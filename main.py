import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import datetime
import requests
import json

load_dotenv()
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
OPENWEATHERMAP_API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET))
bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Halo! Saya adalah bot Telegram sederhana.")


def play_song(update, context):
    song_name = ' '.join(context.args)
    results = sp.search(q=song_name, type='track')
    if len(results['tracks']['items']) > 0:
        track = results['tracks']['items'][0]
        track_name = track['name']
        track_artist = track['artists'][0]['name']
        track_preview_url = track['preview_url']

        if track_preview_url is not None:
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"Memutar lagu {track_name} oleh {track_artist}")
            context.bot.send_audio(chat_id=update.effective_chat.id, audio=track_preview_url)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"Maaf, lagu {track_name} oleh {track_artist} tidak dapat diputar.")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Maaf, lagu {song_name} tidak ditemukan.")


def get_weather(update, context):
    city_name = ' '.join(context.args)
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={OPENWEATHERMAP_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_desc = data['weather'][0]['description']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        message = f"Cuaca di {city_name}:\n{weather_desc}\nSuhu: {temp} °C\nTerasa seperti: {feels_like} °C\nKelembaban: {humidity}%\nKecepatan angin: {wind_speed} m/s"
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Maaf, tidak dapat menemukan kota yang dimaksud.")


def respond_to_message(update, context):
    message = update.message.text
    
    if message.lower() in ['viki', 'piki', 'pik', 'vik', 'ki', 'kii', 'vicky', 'vikii', 'pikii']:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Kenapa manggil manggil Owner Ayaka -,")

    elif message.lower() in ['owner', 'pemilik', 'run']:
        button = InlineKeyboardButton(text="Instagram Owner", url="https://instagram.com/moe.sazumiviki")
        reply_markup = InlineKeyboardMarkup([[button]])
        context.bot.send_message(chat_id=update.effective_chat.id, text="Halo kak, owner Ayaka Sazumi Viki, Kamu bisa kunjungi Instagram owner aku disini", reply_markup=reply_markup)

    elif message.lower() in ['jam', 'waktu', 'hari', 'tanggal']:
        now = datetime.datetime.now()
        new_year_date = datetime.datetime(now.year + 1, 1, 1, 0, 0, 0)
        days_left = (new_year_date - now).days
        message = f"Hari ini tanggal {now.strftime('%d %B %Y')}, pukul {now.strftime('%H:%M:%S')}. Sisa hari menuju tahun baru: {days_left} hari."
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)

    elif message.lower() in ['assalamualaikum', 'salam', 'ass', 'mikum']:
        sender_name = update.message.from_user.first_name
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Waalaikumsalam kak {sender_name}")

    elif any(word in message.lower() for word in ['script', 'sc', 'source', 'code', 'kode sumber']):
        button = InlineKeyboardButton(text="Source Code", url="https://github.com/SazumiVicky/Ayaka-TeleOne")
        reply_markup = InlineKeyboardMarkup([[button]])
        context.bot.send_message(chat_id=update.effective_chat.id, text="Halo, untuk Source Code Ayaka versi TeleOne kamu bisa mendapatkan melalui link berikut:", reply_markup=reply_markup)

    elif message.lower() in ['asu', 'babi', 'anjing', 'memek', 'goblok', 'tolol', 'lol', 'ngakak', 'puki', 'kontol', 'tai', 'bot goblok', 'bot tolol', 'bot anjing', 'gila']:
        sender_name = update.message.from_user.first_name
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Mohon maaf jika Ayaka membuat kamu marah, Ayaka hanya robot yang dikembangkan oleh manusia, Ayaka minta maaf kepada {sender_name} kalau Ayaka mempunyai salah.")

    elif message.lower() in ['hai', 'halo', 'ayaka', 'test', 'woi', 'bot', 'pp', 'p', 'hmm', 'o', 'y', 'g']:
        sender_name = update.message.from_user.first_name
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Halo kak {sender_name}. Ada yang bisa Ayaka bantu?")

    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Maaf, Ayaka Masih Dalam Tahap Pengembangan, Mohon Maaf Kalau Ayaka Tidak Bisa Membantu Anda Untuk Saat ini")


def main():
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    play_song_handler = CommandHandler('play', play_song)
    dispatcher.add_handler(play_song_handler)

    get_weather_handler = CommandHandler('weather', get_weather)
    dispatcher.add_handler(get_weather_handler)

    message_handler = MessageHandler(Filters.text & (~Filters.command), respond_to_message)
    dispatcher.add_handler(message_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()