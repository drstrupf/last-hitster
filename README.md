LastHitster
===========
Personalized [Hitster](https://hitstergame.com/) based on the player's [Last.fm](
https://www.last.fm) scrobbles.


Setup
-----
Requires `docopt`, `pylast`, and `spotipy`. You will need API keys for both, [Last.fm](
https://www.last.fm/api/account/create) and [Spotify](https://developer.spotify.com/dashboard/).
Your Spotify app will likely be in development mode, so you need to add yourself as user. Also
the redirect URI of the Spotify app must match the one in the code. We set it to this repo.

Add your API keys to the environment, e.g. like this in PowerShell:
```
PS> $env:LASTFM_API_KEY = "your-secret-numbers"
PS> $env:LASTFM_API_SECRET = "your-secret-numbers"
PS> $env:SPOTIFY_CLIENT_ID = "your-secret-numbers"
PS> $env:SPOTIFY_CLIENT_SECRET = "your-secret-numbers"
```
Then you should be able to run `PS> python last-hitster.py` 🤞 On the first time it should
open a browser window, to log in with your Spotify account.
