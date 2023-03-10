from dotenv import load_dotenv
import os

load_dotenv('.env')  # This loads the variables from .env

refresh_token = os.getenv("MY_REFRESH_TOKEN")
my_client_id = os.getenv("MY_CLIENT_ID")
my_client_secret = os.getenv("MY_CLIENT_SECRET")


#below given variables can be derived from playlist link. for ex.: https://open.spotify.com/playlist/5SeRSnMKdrkDX0Gi60fI9z?si=136ec6ea697f457b
playlist_url = 'https://api.spotify.com/v1/playlists/5SeRSnMKdrkDX0Gi60fI9z/tracks'
playlist_image_url = 'https://api.spotify.com/v1/playlists/5SeRSnMKdrkDX0Gi60fI9z/images'



# defining the permission type for the token
my_scope = 'playlist-read-private ugc-image-upload playlist-read-collaborative playlist-modify-private playlist-modify-public'
my_redirect_url = 'http://127.0.0.1:9090'
