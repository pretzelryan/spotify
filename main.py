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
    # display relevant user data
    user = sp.me()
    print("\nUser:", user)

    playback = sp.current_playback()
    print("\nPlayback:", playback)

    devices = sp.devices()
    print("\nDevices:", devices)


def start_playback(sp, playlist):
    # set scope and start playback
    sp.auth_manager.scope = "user-modify-playback-state"
    sp.start_playback(device_id=cred.desktop_id, context_uri=playlist)

    # set volume to mute and shuffle (which also ensures repeat) to run in the background
    sp.volume(0)
    sp.shuffle(True)

    print(f"[{datetime.datetime.now()}] Playback started")


def check_playback(sp):
    # callback function to regularly check playback status
    sp.auth_manager.scope = "user-read-playback-state"
    playback = sp.current_playback()

    if playback is None or playback['is_playing'] is False:
        start_playback(sp, cred.playlist_id)
    print(f"[{datetime.datetime.now()}] Playback checked")


def main():
    # boot spotify on start
    os.startfile(cred.spotify_path)

    # make sure spotify has time to properly boot
    time.sleep(10)

    # set up proper scope and initialize spotify object
    scope = "user-read-playback-state"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.client_id, client_secret=cred.client_secret,
                                                   redirect_uri=cred.redirect_uri, scope=scope))

    print(f"[{datetime.datetime.now()}] Initialization Complete")
    schedule = BlockingScheduler()
    schedule.add_job(lambda: check_playback(sp), 'interval', minutes=1)
    schedule.start()


if __name__ == "__main__":
    main()
