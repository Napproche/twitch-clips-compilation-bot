# General config
ROOT_LOCATION = "" # End with / if using a location
DOWNLOAD_LOCATION     = ROOT_LOCATION + "downloads/"
SECRETS_ROOT_LOCATION = ROOT_LOCATION + "secrets/"
THUMBNAILS_LOCATION   = ROOT_LOCATION + "thumbnails/"

# Secrets
TWITCH_SECRETS_FILE         = SECRETS_ROOT_LOCATION + "twitch_secret.json"
YOUTUBE_CLIENT_SECRETS_FILE = SECRETS_ROOT_LOCATION + "youtube_client_secret.json"

# File that will be created for each channel
YOUTUBE_CHANNEL_CREDENTIALS_FILE_NAME = "credentials.json"

DATABASE_LOCATION = ROOT_LOCATION + "videos.db"

BLACKLISTED_CHANNELS = ["DisguisedToastHS", "xChocoBars", "pokimane", "LilyPichu"]

# Thumbnails
TITLE_FONT_LOCATION = "CFB1 American Captain.otf"
TITLE_SIZE = 70
TITLE_FONT_COLOR = (255, 232, 0)

NUMBER_FONT_LOCATION = "accid_.ttf"
NUMBER_SIZE = 100
NUMBER_FONT_COLOR = 'red'