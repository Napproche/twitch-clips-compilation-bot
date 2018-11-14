# twitch-clip-compilation-creator
Bot that can create compilation videos of:
    - Most popular clips of the day
    - Most popular clips of the week
    - Most popular clips of the month
    - Popular clips of a channel (Will create compilation when there are enough clips collected from a specific Twitch channel)

This bot is currently being used for this YouTube channel: 
- Fortnite: https://www.youtube.com/channel/UCxavrT2r-9tsliwOsmRVZ7w

## Setup

- ```sudo apt-get update```
- ```apt install python3.6```
- ```apt install python3-pip```
- ```pip3 install -r requirements.txt```
- ```pip3 install --upgrade google-auth-oauthlib```
- ```apt-get install imagemagick```
- ```sudo add-apt-repository ppa:kirillshkrogalev/ffmpeg-next```
- ```sudo apt-get install ffmpeg```

## Fonts
Install fonts in `/usr/local/share/fonts` and reboot.

### Secrets

- Create secrets directory in root.
- Create `secrets/youtube_client_credentials.json` with your Installed App credentials from the [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
- Create `secrets/twitch_secret.json` file with contents:
```
{
    "client_id": "YOUR_ID"
}
``` 

### Cron job example
Make sure the path matches the ROOT_LOCATION in the constants.py
```
# Fortnite Highlights Creator channel
0 18 * * * python3 /root/twitch-clip-publisher/bot.py fhc Fortnite day 8
0 1 * * 0 python3 /root/twitch-clip-publisher/bot.py fhc Fortnite week 8
0 2 1 * * python3 /root/twitch-clip-publisher/bot.py fhc Fortnite month 8
```

### Common issues
https://github.com/Zulko/moviepy/issues/401#issuecomment-278679961
https://github.com/Zulko/moviepy/issues/378#issuecomment-274163535

### Assets
#### YouTube Client
https://developers.google.com/api-client-library/python/samples/samples