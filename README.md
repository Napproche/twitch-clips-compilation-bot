# twitch-clip-publisher
Bot that creates and uploads compilations of popular Twitch clips each day.

Live running example of this bot: https://www.youtube.com/channel/UCxavrT2r-9tsliwOsmRVZ7w

The bot takes 4 parameters:
- Channel: Which YouTube channel it will be uploaded on.
- Game: The name of the game from which to fetch clips from.
- Period: The clips can be sorted on most popular of day/week/month.
- Amount of clips: Amount of clips in the compilation video. A 2GB VPS can handle rendering 8-10 clips without running out of memory.

## Setup

- ```sudo apt-get update```
- ```pip install -r requirements.txt```
- ```apt install python3.6```
- ```apt install python3-pip```
- ```pip3 install --upgrade google-auth-oauthlib```
- ```apt-get install imagemagick```
- ```sudo add-apt-repository ppa:kirillshkrogalev/ffmpeg-next```
- ```sudo apt-get install ffmpeg```

### Secrets

- Create secrets directory in root.
- Create `secrets/twitch_secret.json` file with contents:
```
{
    "client_id": "YOUR_ID"
}
``` 
- Create `secrets/youtube_client_credentials.json` with your Installed App credentials from the [Google Cloud Console](https://console.cloud.google.com/apis/credentials)

### Cron jobs
Make sure the path matches the ROOT_LOCATION in the constants.py
- ```0 17 * * * python3 /root/twitch-clip-publisher/script.py day Fortnite 10```
- ```0 17 * * 0 python3 /root/twitch-clip-publisher/script.py week Fortnite 10```
- ```0 0 1 * * python3 /root/twitch-clip-publisher/script.py month Fortnite 10```

### Common issues
https://github.com/Zulko/moviepy/issues/401#issuecomment-278679961

### Assets
#### YouTube Client
https://developers.google.com/api-client-library/python/samples/samples