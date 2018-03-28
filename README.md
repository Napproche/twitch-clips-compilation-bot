# twitch-clip-publisher
Bot that creates and uploads compilations of popular Twitch clips each day.

Live running example of this bot: https://www.youtube.com/channel/UCxavrT2r-9tsliwOsmRVZ7w

## YouTube Client
https://developers.google.com/api-client-library/python/samples/samples

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
- Create `secrets/youtube_channel_credentials.json` with your Installed App credentials from the [Google Cloud Console](https://console.cloud.google.com/apis/credentials)

### Cron job
```30 2 * * * python3 /root/twitch-clip-publisher/script.py```
(Make sure the path matches the ROOT_LOCATION in the constants.py)

### Common issues
https://github.com/Zulko/moviepy/issues/401#issuecomment-278679961