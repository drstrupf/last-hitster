"""
LastHitster

Personalized Hitster based on the player's scrobbles.

Usage:
  last-hitster.py --players <player>...

Options:
  -h --help     Show this screen.
  --players     Last.fm user names.

"""

import os
from collections import defaultdict
from random import choice

from docopt import docopt
import pylast
import spotipy


arguments = docopt(__doc__)

LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")
LASTFM_API_SECRET = os.getenv("LASTFM_API_SECRET")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

EXCLUDED_WORDS = ["intro", "live", "cover", "remix", "re-mix"]

artists = set()
dict_of_shame = defaultdict(set)
network = pylast.LastFMNetwork(LASTFM_API_KEY, LASTFM_API_SECRET)
for player in arguments["<player>"]:
    user = network.get_user(player)
    players_top_artists = user.get_top_artists(limit=100)
    artists = artists.union(players_top_artists)
    for artist in players_top_artists:
        dict_of_shame[artist.item.get_name()].add(player)

sp = spotipy.Spotify(
    auth_manager=spotipy.SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri="https://github.com/drstrupf/last-hitster",
        scope="user-read-playback-state,user-modify-playback-state",
        open_browser=True,
    )
)

while True:
    input("Press Enter to play next song")
    track_found = False
    while not track_found:
        artist = choice(list(artists))
        track = choice(artist.item.get_top_tracks(limit=10))
        items = sp.search(
            f"artist:{artist.item.get_name()} track:{track.item.get_name()}"
        )["tracks"]["items"]
        filtered_items = [
            item
            for item in items
            if not any(word in item["name"].lower() for word in EXCLUDED_WORDS)
        ]
        track_found = len(filtered_items) > 0
    track = filtered_items[0]

    while not any(device["is_active"] for device in sp.devices()["devices"]):
        input("Activate a Spotify device by playing a song and press Enter")
    sp.start_playback(uris=[track["uri"]])

    input("Press Enter to reveal song")
    artist_names = ", ".join(artist["name"] for artist in track["artists"])
    year = track["album"]["release_date"][:4]
    print(f"  {track['name']} by {artist_names} ({year})")
    print(f"  Thanks {', '.join(dict_of_shame[artist.item.get_name()])}!")

    input("Press Enter to pause")
    if sp.currently_playing()["is_playing"]:
        sp.pause_playback()
