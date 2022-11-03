# ATuaMae
## Discord Bot

@ author gm0l74<br />
@ updated 03-11-2022<br />

# APIs

## Discord Token

To know more about the creation a Discord Bot in the Discord Developer Portal,
please refer to the following link:
https://realpython.com/how-to-make-a-discord-bot-python/

The obtained token should be inserted in the '.env' file in the project's root
directory, as an evironment variable named <DISCORD_TOKEN>.

## Spotify App Credentials

Obtain the the *CLIENT_ID* and *CLIENT_SECRET* from the Spotify Developer Dashboard,
please refer to the following link:
https://developer.spotify.com/dashboard/login

Such credentials should be included in the '.env' file in the project's root,
as evironment variables named <SPOTIFY_CLIENT_ID> and <SPOTIFY_SECRET>.

Consult the documentation of the Spotify API for Python at the following link:
https://spotipy.readthedocs.io/en/2.21.0/

# Installation

It is advised to use a virtual environment to install the dependencies.
To create a virtual environment, please refer to the following link:
https://docs.python.org/3/library/venv.html

```bash
# To create...
$ python3 -m venv venv

# To activate...
$ source venv/bin/activate
```
```

To install the python-related dependencies, run the following command in the terminal:

```bash
$ make install
```

The project uses the *Opec Audio Codec* to process music streams from youtube.
To install the Opec Audio Codec, run the following command in the terminal:

```bash
# ---------------- macOS ----------------
$ brew install opus

# ---------------- linux ----------------
# 1. Install the opus-tools:
$ sudo apt-get install opus-tools

# 2. Install the libav-tools:
$ sudo apt-get install libav-tools
```

*ffmpeg* is also required.
To install it, run the following command in the terminal:

```bash
# for macOS
$ brew install ffmpeg

# for Linux
$ sudo apt install ffmpeg 
```

# Run the Bot

To run the bot, simply do:

```bash
$ python3 main.py
```