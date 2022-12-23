"""
Testing env for spotify API shenanigans
"""

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import cred


def print_recently_played(sp):
    sp.auth_manager.scope = "user-read-recently-played"
    recently_played = sp.current_user_recently_played()
    for idx, item in enumerate(recently_played['items']):
        track = item['track']
        print(idx, track['artists'][0]['name'], " – ", track['name'])


def create_playlist(sp, user, name="test"):
    sp.auth_manager.scope = "playlist-modify-private"
    sp.user_playlist_create(user['id'], name, public=False)


def main():
    scope = "user-read-playback-state"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.client_id, client_secret=cred.client_secret,
                                                   redirect_uri=cred.redirect_uri, scope=scope))
    user = sp.me()
    playback = sp.current_playback()
    print("\nUser:", user)
    print("\nPlayback:", playback)

    if playback is None or playback['is_playing'] is False:
        try:
            sp.auth_manager.scope = "user-modify-playback-state"
            sp.start_playback(device_id=playback['device']['id'])
        except:
            print("Error Occured")


if __name__ == "__main__":
    main()
