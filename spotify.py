import spotipy
import spotipy.util as util
from telebot import types
import requests


class Spotify():
    def __init__(self):
        self.__SPOTIFY = spotipy.Spotify(auth=util.prompt_for_user_token('test', client_id='5f2ed853c47f48a9a6a710510419d81b',
                                                                    client_secret='ee076258b2674933a84ccfdeb0b14f1d', redirect_uri='https://google.com'))

    def search_artist(self, artist_name):
        searched_artist = self.__SPOTIFY.search(
            artist_name.lower(),
            limit=1,
            offset=0,
            type='artist'
            )
        if not searched_artist['artists']['items']:
            return None
        return Artist(searched_artist)
    
    def search_track(self, track_name):
        searched_track = self.__SPOTIFY.search(
            track_name.lower(),
            limit=1,
            offset=0,
            type='track'
            )
        if not searched_track['tracks']['items']:
            return None
        else:
            return Track(searched_track)
    
    def make_search_button(self):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_artist_search = types.KeyboardButton('Поиск артиста')
        button_track_search = types.KeyboardButton('Поиск трека')
        keyboard.add(button_artist_search, button_track_search)
        return keyboard


class Artist:
    def __init__(self, artist_data):
        self.name = artist_data['artists']['items'][0]['name']
        self.link = artist_data['artists']['items'][0]['external_urls']['spotify']
        self.pic = artist_data['artists']['items'][0]['images'][1]['url']
        self.albums = None
        self.button = self.make_artist_url_button(self.link)

    def make_artist_url_button(self, url):
        inline_keyboard = types.InlineKeyboardMarkup()
        artist_in_spotify = types.InlineKeyboardButton('Открыть на Spotify', url=url)
        inline_keyboard.add(artist_in_spotify)
        return inline_keyboard


class Track:
    def __init__(self, track_data):
        self.name = track_data['tracks']['items'][0]['name']
        self.link = track_data['tracks']['items'][0]['external_urls']['spotify']
        self.pic_album = track_data['tracks']['items'][0]['album']['images'][1]['url']
        self.album_link = track_data['tracks']['items'][0]['album']['external_urls']['spotify']
        self.album_name = track_data['tracks']['items'][0]['album']['name']
        self.preview_url = track_data['tracks']['items'][0]['preview_url']
        self.id = track_data['tracks']['items'][0]['id']
        self.keyboard = self.make_track_url_button(self.link, self.id)
        self.caption = '{0}\n\nАльбом: [{1}]({2})'.format(self.name, self.album_name, self.album_link)
    
    def make_track_url_button(self, url, track_id):
        inline_keyboard = types.InlineKeyboardMarkup()
        track_in_spotify = types.InlineKeyboardButton('Открыть на Spotify', url=url)
        track_preview = types.InlineKeyboardButton('Превью трека', callback_data=track_id)
        inline_keyboard.add(track_in_spotify, track_preview)
        return inline_keyboard
