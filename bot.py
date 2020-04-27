import telebot as tb
import spotify
from to_json import to_json


bot = tb.TeleBot('940145749:AAENwzTWDnBkbCXwJZ8Fw7XdS0GCM5CgZoU', threaded=False)
spotify_client = spotify.Spotify()
track_data = {}


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(
        chat_id=message.chat.id,
        text='Привет.\nПока что я умею искать только артистов и треки',
        reply_markup=spotify_client.make_search_button()
        )


@bot.message_handler(func=lambda message: message.text.lower() == 'поиск артиста')
def get_artist_name(message):
    bot.send_message(chat_id=message.chat.id, text='Кого искать?')
    bot.register_next_step_handler(message, search_artist)

def search_artist(message):
        artist = spotify_client.search_artist(message.text)
        if artist is None:
            bot.send_message(chat_id=message.chat.id, text='Ничего не нашел')
        else:
            bot.send_photo(chat_id=message.chat.id, photo=artist.pic,
                           caption=artist.name, reply_markup=artist.button)


@bot.message_handler(func=lambda message: message.text.lower() == 'поиск трека')
def get_track_name(message):
    bot.send_message(chat_id=message.chat.id, text='Какой трек искать?')
    bot.register_next_step_handler(message, search_track)

def search_track(message):
    track = spotify_client.search_track(message.text)
    if track is None:
        bot.send_message(chat_id=message.chat.id, text='Ничего не нашел')
    else:
        bot.send_photo(chat_id=message.chat.id, photo=track.pic_album,
                       caption=track.caption, reply_markup=track.keyboard, parse_mode='markdown')
        global track_data
        track_data[track.id] = track.preview_url


@bot.callback_query_handler(func=lambda query: True)
def query_handler(query):
    if query.data in track_data.keys():
        bot.send_audio(chat_id=query.message.chat.id, audio=track_data[query.data])


bot.polling()

