# twitch-clip-publisher
Bot that creates and uploads compilations of popular Twitch clips each day.

Bot is used for these channels: 
- Fortnite: https://www.youtube.com/channel/UCxavrT2r-9tsliwOsmRVZ7w
- PUBG: https://www.youtube.com/channel/UCs89cVeXqCfs1uN2FXsKgNA
- Rocket League: https://www.youtube.com/channel/UCyID9pf6qVvSXQfupMPza2A
- Hearthstone: https://www.youtube.com/channel/UCzPGjHAZeUxrx1tl3Rg81QA

The bot takes 4 parameters:
- Channel: Channel name to upload to.
- Game: The name of the game.
- Period: day/week/month.
- Amount of clips: Amount of clips that will be rendered. 

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

### Common issues
https://github.com/Zulko/moviepy/issues/401#issuecomment-278679961

### Assets
#### YouTube Client
https://developers.google.com/api-client-library/python/samples/samples