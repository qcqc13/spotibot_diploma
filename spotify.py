import spotipy
import spotipy.util as util


def auth():
    return spotipy.Spotify(auth=util.prompt_for_user_token('test', client_id='5f2ed853c47f48a9a6a710510419d81b',
                                                            client_secret='ee076258b2674933a84ccfdeb0b14f1d', redirect_uri='https://google.com'))


def search_artist(spotify, artist_name):
    searched_artist = spotify.search(artist_name.lower(),
                             limit=1, offset=0, type='artist')
    if not searched_artist['artists']['items']:
        return None
    return search_artist


class Artist:
    def __init__(self, artist_data):
        self.name = artist_data['artists']['items'][0]['name']
        self.link = artist_data['artists']['items'][0]['external_urls']['spotify']
        self.pic = artist_data['artists']['items'][0]['images'][1]['url']
        self.albums = None
