# General config
ROOT_LOCATION = "" # End with / if using a location
SECRETS_ROOT_LOCATION = ROOT_LOCATION + "secrets/"
ASSETS_LOCATION = ROOT_LOCATION + "assets/"
DOWNLOAD_LOCATION = ASSETS_LOCATION + "downloads/"
THUMBNAILS_LOCATION = ASSETS_LOCATION + "thumbnails/"

# Secrets
TWITCH_SECRETS_FILE         = SECRETS_ROOT_LOCATION + "twitch_secret.json"
YOUTUBE_CLIENT_SECRETS_FILE = SECRETS_ROOT_LOCATION + "youtube_client_secret.json"

# File that will be created for each channel
YOUTUBE_CHANNEL_CREDENTIALS_FILE_NAME = "credentials.json"

DATABASE_LOCATION = ROOT_LOCATION + "database.db"

BLACKLISTED_CHANNELS = ["DisguisedToastHS", "xChocoBars", "pokimane", "LilyPichu"]

# Thumbnails
FONTS_LOCATION = ASSETS_LOCATION + "fonts/"
LOGOS_LOCATION = ASSETS_LOCATION + "logos/"

TITLE_FONT_LOCATION = FONTS_LOCATION + "BurbankBigCondensed-Bold.otf"
TITLE_SIZE = 70
TITLE_FONT_COLOR = (255, 232, 0)
TITLE_BORDER_THICKNESS = 3

NUMBER_FONT_LOCATION = FONTS_LOCATION + "accid_.ttf"
NUMBER_SIZE = 100
NUMBER_FONT_COLOR = 'red'
NUMBER_BORDER_THICKNESS = 2
