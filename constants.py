# General config
ROOT_LOCATION = "" # End with / if using a location
DOWNLOAD_LOCATION     = ROOT_LOCATION + "downloads/"
SECRETS_ROOT_LOCATION = ROOT_LOCATION + "secrets/"

# Secrets
TWITCH_SECRETS_FILE         = SECRETS_ROOT_LOCATION + "twitch_secret.json"
YOUTUBE_CLIENT_SECRETS_FILE = SECRETS_ROOT_LOCATION + "youtube_client_secret.json"

# File that will be created for each channel
YOUTUBE_CHANNEL_CREDENTIALS_FILE_NAME = "credentials.json"

DATABASE_LOCATION = ROOT_LOCATION + "videos.db"

BLACKLISTED_CHANNELS = ["DisguisedToastHS", "xChocoBars", "pokimane", "lilypichu"]