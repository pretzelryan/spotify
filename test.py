"""
Testing env for spotify API shenanigans
"""

import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
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
    # boot spotify on start
    os.startfile(cred.spotify_path)

    # make sure spotify has time to properly boot
    time.sleep(10)

    scope = "user-read-playback-state"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.client_id, client_secret=cred.client_secret,
                                                   redirect_uri=cred.redirect_uri, scope=scope))

    user = sp.me()
    playback = sp.current_playback()
    print("\nUser:", user)
    print("\nPlayback:", playback)

    devices = sp.devices()
    print(devices)

    # if playback is None or playback['is_playing'] is False:
    #     try:
    #         sp.auth_manager.scope = "user-modify-playback-state"
    #         sp.start_playback(device_id=playback['device']['id'])
    #     except:
    #         print("Error Occured")

    # sp.auth_manager.scope = "user-modify-playback-state"
    # sp.start_playback(device_id=cred.desktop_id, context_uri=cred.playlist_id)

    # set volume to mute and shuffle (which also ensures repeat) to run in the background
    # sp.volume(0)
    # sp.shuffle(True)


if __name__ == "__main__":
    main()
