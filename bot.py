import telebot as tb
import proxy_changer
import spotipy
import spotipy.util as util
import custom_keyboard
from to_json import to_json



proxy = proxy_changer.read_proxy()
bot = tb.TeleBot('940145749:AAENwzTWDnBkbCXwJZ8Fw7XdS0GCM5CgZoU', threaded=False)
tb.apihelper.proxy = proxy_changer.set_proxy(proxy)
spotify = spotipy.Spotify(auth=util.prompt_for_user_token('test', client_id='5f2ed853c47f48a9a6a710510419d81b', client_secret='ee076258b2674933a84ccfdeb0b14f1d', redirect_uri='https://google.com'))

user_data = {}


@bot.message_handler(commands=['start'])
def welcome(message):
    #keyboard = custom_keyboard.make_top_50()
   # bot.send_message(message.chat.id, 'Выбери список Топ-50 песен или Топ 50 артистов', reply_markup=keyboard)
    bot.send_message(message.chat.id, 'Если нужно найти исполнителя – напиши его имя и фамилию')


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'топ 50 песен':
        top_50_tracks = tracks_top50.get_top_tracks()
        msg = tracks_top50.preparing_message(top_50_tracks['tracks']['track'])
        user_data[message.chat.id] = msg
        inline_keyboard = custom_keyboard.make_navigator(without_button='left')
        bot.send_message(message.chat.id, msg[0], reply_markup=inline_keyboard,
                         disable_web_page_preview=True, parse_mode='markdown')

    elif message.text.lower() == 'топ 50 артистов':
        top_50_artists = artists_top50.get_top_artist()
        msg = artists_top50.preparing_message(top_50_artists['artists']['artist'])
        user_data[message.chat.id] = msg
        inline_keyboard = custom_keyboard.make_navigator(without_button='left')
        bot.send_message(message.chat.id, msg[0], reply_markup=inline_keyboard,
                         disable_web_page_preview=True, parse_mode='markdown')

    else:
        results = spotify.search(message.text.lower(), limit=1, offset=0, type='artist')
        if not results['artists']['items']:
            bot.send_message(message.chat.id, 'Ничего не нашел')
        else:
            name_artist = results['artists']['items'][0]['name']
            link_artist = results['artists']['items'][0]['external_urls']['spotify']
            pic_artist = results['artists']['items'][0]['images'][1]['url']
            open_spotify = custom_keyboard.button_open_in_spotify(link_artist)
            bot.send_photo(message.chat.id, pic_artist, name_artist, reply_markup=open_spotify)
            to_json(results)


@bot.callback_query_handler(func=lambda query: True)
def callback_handler(query):
    chat_id = query.message.chat.id

    if query.data == 'next':
        keyboard = custom_keyboard.make_navigator(without_button='right')
        bot.answer_callback_query(query.id, 'Вторая страница')
        bot.edit_message_text(user_data[chat_id][1], chat_id, query.message.message_id,
                              parse_mode='Markdown', disable_web_page_preview=True, reply_markup=keyboard)
    elif query.data == 'prev':
        keyboard = custom_keyboard.make_navigator(without_button='left')
        bot.answer_callback_query(query.id, 'Первая страница')
        bot.edit_message_text(user_data[chat_id][0], chat_id, query.message.message_id,
                              parse_mode='Markdown', disable_web_page_preview=True, reply_markup=keyboard)


try:
    # Запускаем бота
    bot.polling()

# Если прокси отваливается
except OSError:
    bot.stop_polling()

    proxy = proxy_changer.get_proxy()
    proxy_changer.write_proxy(proxy)

    bot.polling()
