# twitch-clip-publisher
Bot that creates and uploads compilations of popular Twitch clips each day/week/month

## YouTube Client
https://developers.google.com/api-client-library/python/samples/samples

## Setup
`apt install python3.6`
`apt install python3-pip`
`pip install -r requirements.txt`
`apt-get install imagemagick`

### Secrets

- Create secrets directory in root.
- Create `secrets/twitch_secret.json` file with contents:
```
{
    "client_id": "YOUR_ID"
}
``` 
- Create `secrets/youtube_channel_credentials.json` with your Installed App credentials.

### Install FFMPEG
```
sudo add-apt-repository ppa:kirillshkrogalev/ffmpeg-next
sudo apt-get update
sudo apt-get install ffmpeg
```

`pip3 install --upgrade google-auth-oauthlib`


Fixes:
https://github.com/Zulko/moviepy/issues/401#issuecomment-278679961