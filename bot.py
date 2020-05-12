import telebot as tb
import spotify
import logging
from to_json import to_json
import proxy_changer


proxy = proxy_changer.read_proxy()
bot = tb.TeleBot('940145749:AAENwzTWDnBkbCXwJZ8Fw7XdS0GCM5CgZoU', threaded=False)
tb.apihelper.proxy = proxy_changer.set_proxy(proxy)
spotify_client = spotify.Spotify()
track_data = {}
# настройка логера
bot_logger = logging.getLogger('bot')
logging.basicConfig(filename='bot.log', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%d.%m.%Y %H:%M')


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
            bot_logger.info('Artist "{}" not found, user – {}\n'.format(message.text,
                                                                    message.from_user.username))
        else:
            bot.send_photo(chat_id=message.chat.id, photo=artist.pic,
                           caption=artist.name, reply_markup=artist.button)
            bot_logger.info('Artist "{}" found, user – {}\n'.format(message.text,
                                                                    message.from_user.username))


@bot.message_handler(func=lambda message: message.text.lower() == 'поиск трека')
def get_track_name(message):
    bot.send_message(chat_id=message.chat.id, text='Какой трек искать?')
    bot.register_next_step_handler(message, search_track)

def search_track(message):
    track = spotify_client.search_track(message.text)
    if track is None:
        bot.send_message(chat_id=message.chat.id, text='Ничего не нашел')
        bot_logger.info('Track "{}" not found, user – {}\n'.format(message.text,
                                                                   message.from_user.username))
    else:
        bot.send_photo(chat_id=message.chat.id, photo=track.pic_album,
                       caption=track.caption, reply_markup=track.keyboard, parse_mode='markdown')
        global track_data
        track_data[track.id] = track
        bot_logger.info('Track "{}" found, user – {}\n'.format(message.text,
                                                               message.from_user.username))


@bot.callback_query_handler(func=lambda query: True)
def query_handler(query):
    if query.data in track_data.keys():
        track = track_data[query.data]
        bot.send_audio(chat_id=query.message.chat.id, audio=track.preview_url,
                       caption=track.name)
        bot_logger.info('Track preview was sent')
    else:
        bot.send_message(query.message.chat.id, 'Не могу найти этот трек у себя')
        bot_logger.warning('Track preview wasn`t sent, not found id')


try:
    bot.polling()
except OSError:
    bot.stop_polling()
    proxy = proxy_changer.get_proxy()
    proxy_changer.write_proxy(proxy)
    bot.polling()

