from .library import *

admin_user_id = 1234 #<---- آیدی عددی شما
api_id = 1234 #<---- api آیدی شما
api_hash = 'abcdefgh1234'  #<---- api هش شما
client_id = '01e7dc6b41c3471b94efe87abeb05919'
client_secret = '4f5f93af1ced4b0d9ba8440606803639'

client = TelegramClient('TRself-MT', api_id, api_hash)
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
