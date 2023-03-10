"""Year of the Cat spotify playlist's backend. Link to the playlist: https://open.spotify.com/playlist/5SeRSnMKdrkDX0Gi60fI9z?si=136ec6ea697f457b


Use this file just one time to get your refresh token.

Author: Elchin Aslanli
Date: March 12, 2023
"""

import config
import webbrowser
from urllib.parse import urlencode


auth_headers = {
    "client_id": config.my_client_id,
    "response_type": "code",
    "redirect_uri": config.my_redirect_url,
    "scope": config.my_scope
}

webbrowser.open("https://accounts.spotify.com/authorize?" + urlencode(auth_headers)) # it returns the refresh token
