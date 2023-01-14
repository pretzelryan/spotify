"""
main file for farming spotify minutes
"""


import time
import datetime
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from apscheduler.schedulers.blocking import BlockingScheduler
import cred


def disp_user(sp):
    user = sp.me()
    print("\nUser:", user)

    playback = sp.current_playback()
    print("\nPlayback:", playback)

    devices = sp.devices()
    print("\nDevices:", devices)


def start_playback(sp, playlist):
    # function to start a playback of selected playlist
    try:
        sp.auth_manager.scope = "user-modify-playback-state"
        sp.start_playback(device_id=cred.desktop_id, context_uri=playlist)
        sp.volume(0, device_id=cred.desktop_id)
        sp.shuffle(True, device_id=cred.desktop_id)
        sp.repeat('context', device_id=cred.desktop_id)
        print(f"[{datetime.datetime.now()}] NOTICE: Playback started")

    except spotipy.exceptions.SpotifyException as e:
        print(f"[{datetime.datetime.now()}] Spotify Exception Occurred\n", e)


def check_playback(sp):
    # callback function to regularly check playback status
    sp.auth_manager.scope = "user-read-playback-state"
    playback = sp.current_playback()

    print(f"[{datetime.datetime.now()}] Playback checked")
    if playback is None or playback['is_playing'] is False:
        start_playback(sp, cred.playlist_id)


def main():
    # start spotify application
    os.startfile(cred.spotify_path)
    time.sleep(10)

    # set up proper scope and initialize spotify object
    scope = "user-read-playback-state"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.client_id, client_secret=cred.client_secret,
                                                   redirect_uri=cred.redirect_uri, scope=scope))

    # after initialization, create schedule to check playback
    print(f"[{datetime.datetime.now()}] Initialization Complete")
    schedule = BlockingScheduler()
    schedule.add_job(lambda: check_playback(sp), 'interval', minutes=1)
    schedule.start()


if __name__ == "__main__":
    main()
