from config_updater import update_config
from time import sleep
import telebot as tb
import configparser
import spotify
import logging
import hashlib



config = configparser.ConfigParser()
config.read('./config.ini')
bot = tb.TeleBot(config['bot']['token'], threaded=False)
spotify_client = spotify.Spotify()
track_data = {}
search_state = config['bot']['search_state']
bot_logger = logging.getLogger(config['logger']['title'])
logging.basicConfig(filename=config['logger']['filename'], level=logging.INFO,
                    format=config['logger']['text_format'],
                    datefmt=config['logger']['date_format'])


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(
        chat_id=message.chat.id,
        text='Привет.\nПока что я умею искать только артистов и треки',
        reply_markup=spotify_client.make_search_button()
        )


@bot.message_handler(commands=['log'])
def send_log(message):
    user_id = '{}'.format(message.from_user.id)
    hex_user_id = hashlib.sha256(user_id.encode('utf-8')).hexdigest()
    if hex_user_id in config['permissions']['log_permissions']:
        log = open('./bot.log')
        bot.send_document(message.chat.id, log)
    else:
        bot.send_message(message.chat.id, 'У вас нет доступа к логу')


@bot.message_handler(content_types=config['bot']['exclusive_content_types'])
def sticker(message):
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIHZF7Hth0YOndd71fohOEqcSniJ4fcAAL_BwAC-gu2CMha9691__jVGQQ')


@bot.message_handler(func=lambda message: message.text.lower() == 'поиск артиста')
def set_state_search_artist(message):
    global search_state
    search_state = 'artist'
    bot.send_message(message.chat.id, 'Какого артиста искать?')
    config.set('bot', 'search_state', 'artist')
    update_config('./config.ini', config)


@bot.message_handler(func=lambda message: message.text.lower() == 'поиск трека')
def set_state_search_track(message):
    global search_state
    search_state = 'track'
    bot.send_message(message.chat.id, 'Какой трек искать?')
    config.set('bot', 'search_state', 'track')
    update_config('./config.ini', config)


@bot.message_handler(content_types=['text'])
def main(message):
    if search_state == 'artist':
        search_artist(message)
    elif search_state == 'track':
        search_track(message)
    else:
        bot.send_message(message.chat.id, 'Нужно искать треки или артистов?',
                         reply_markup=spotify_client.make_search_button())

def search_artist(message):
        artist = spotify_client.search_artist(message.text)
        if artist is None:
            bot.send_message(chat_id=message.chat.id, text='Ничего не нашел')
            bot_logger.info('Artist "{}" not found, user – {}'.format(message.text,
                                                                    message.from_user.username))
        else:
            bot.send_photo(chat_id=message.chat.id, photo=artist.pic,
                           caption=artist.name, reply_markup=artist.button)
            bot_logger.info('Artist "{}" found, user – {}'.format(message.text,
                                                                    message.from_user.username))

def search_track(message):
    track = spotify_client.search_track(message.text)
    if track is None:
        bot.send_message(chat_id=message.chat.id, text='Ничего не нашел')
        bot_logger.info('Track "{}" not found, user – {}'.format(message.text,
                                                                   message.from_user.username))
    else:
        bot.send_photo(chat_id=message.chat.id, photo=track.pic_album,
                       caption=track.caption, reply_markup=track.keyboard, parse_mode='markdown')
        global track_data
        track_data[track.id] = track
        bot_logger.info('Track "{}" found, user – {}'.format(message.text,
                                                             message.from_user.username))


@bot.callback_query_handler(func=lambda query: True)
def query_handler(query):
    if query.data in track_data.keys():
        track = track_data[query.data]
        bot.send_audio(chat_id=query.message.chat.id, audio=track.preview_url,
                       caption=track.name)
        bot_logger.info('Track preview was sent')
    else:
        bot.send_message(query.message.chat.id, 'Не могу найти превью трека')
        bot_logger.warning('Track preview wasn`t sent, not found id')


try:
    bot.polling()
except OSError:
    bot_logger.exception('Disconnected, restart bot in 10 seconds')
    sleep(10)
    bot.stop_polling()
    bot.polling()