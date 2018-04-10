from PIL import Image, ImageFont, ImageDraw
import constants
from urllib import request
import re

def create(clip, number, channel, game, period):
    """
        Creates a thumbnail image from a clip and a video number.
    """
    name = removeSpaces(channel + '_' + game + '_' + period + '_' + str(number)) + '.png'
    path = constants.THUMBNAILS_LOCATION + name

    downloadThumbnailFromURL(clip['thumbnail'], path)
    
    title = addNewLineAfterXChars(clip['title'])

    addTitle(title, path)
    addNumber(number, path)
    addGameIcon(game, path)      

    return path

def addTitle(title, path):
    img = Image.open(path)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(constants.TITLE_FONT_LOCATION, constants.TITLE_SIZE)
    
    x, y = 10, 10

    thickness = constants.TITLE_BORDER_THICKNESS

    # Draw a small black border around the text to make it more readable.
    draw.text((x-thickness, y-thickness), title, font=font, fill='black')
    draw.text((x+thickness, y-thickness), title, font=font, fill='black')
    draw.text((x-thickness, y+thickness), title, font=font, fill='black')
    draw.text((x+thickness, y+thickness), title, font=font, fill='black')

    # Draw the title.
    draw.text((x, y), title, constants.TITLE_FONT_COLOR, font=font)
    
    img.save(path)

def addNumber(number, path):
    number = "#" + str(number)

    img = Image.open(path)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(constants.NUMBER_FONT_LOCATION, constants.NUMBER_SIZE)
    
    x, y = 300, 150

    thickness = constants.NUMBER_BORDER_THICKNESS

    # Draw a small black border around the text to make it more readable.
    draw.text((x-thickness, y-thickness), number, font=font, fill='black')
    draw.text((x+thickness, y-thickness), number, font=font, fill='black')
    draw.text((x-thickness, y+thickness), number, font=font, fill='black')
    draw.text((x+thickness, y+thickness), number, font=font, fill='black')

    # Draw the number.
    draw.text((x, y), number, constants.NUMBER_FONT_COLOR, font=font)
    
    img.save(path)

def addGameIcon(game, path):
    background = Image.open(path)
    foreground = Image.open(constants.LOGOS_LOCATION + game + '.png')

    background.paste(foreground, (20, 120), foreground)
    background.save(path, format="png")

def downloadThumbnailFromURL(url, location):
    print('Downloading thumbnail: ' + url)
    f = open(location, 'wb')
    f.write(request.urlopen(url).read())
    f.close()

def removeSpaces(string):
    return string.replace(" ", "_")

def addNewLineAfterXChars(string):
    """
        Add a newline after 18 characters. Counted for 70pt font.
    """
    return re.sub("(.{18})", "\\1\n", string, 0, re.DOTALL)