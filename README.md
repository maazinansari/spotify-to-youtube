# What is this? 

This project is an attempt to transfer music tracks from a Spotify playlist to a YouTube playlist. 
Spotify and Google offer free tools for developers that make this easy. 

# Setup

## Spotify

1. You should already have a Spotify account and tracks saved in a playlist
1. Generate developer API keys
1. Add the API keys to your environment variables

## Google/YouTube

1. Follow the directions here: https://developers.google.com/youtube/v3/getting-started
1. Create OAuth

Since this is meant to be a one-time script for me, and since Google limits the number of projects a user can have, 
I am not creating a new project for this. 
Instead I am creating OAuth credentials under my pacificleaguetv-summary project. 

## Python (these scripts)

The following libraries are required

- spotipy
- [googleapiclient.discovery](https://github.com/googleapis/google-api-python-client?tab=readme-ov-file#installation)

Install them in a virtual environment

1. `python3 -m venv spytenv3`
1. `source spytenv3/bin/activate`
1. `spytenv3/bin/pip install google-api-python-client`
1. `spytenv3/bin/pip install spotipy`
1. `spytenv3/bin/pip install google_auth_oauthlib`
1. `spytenv3/bin/pip install --upgrade google-api-python-client`
1. `spytenv3/bin/pip install --upgrade google-auth-oauthlib google-auth-httplib2`
